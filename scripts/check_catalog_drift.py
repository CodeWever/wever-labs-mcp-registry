#!/usr/bin/env python3
"""Read-only regression check for registry, website and live MCP catalog drift.

Run directly for local registry + public website verification. Add --published
to also verify the registry files currently served by GitHub main.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ORIGIN = 'https://weverlabs.com'
MAIN = ORIGIN + '/mcp'
FREE = ORIGIN + '/mcp-free'
PUBLIC_REGISTRY = 'https://raw.githubusercontent.com/CodeWever/wever-labs-mcp-registry/main/'
REGISTRY_FILES = ('server.json', 'server.dns-auth.example.json', 'lhm.plugin.json',
                  'README.md', 'REGISTRY_COPY_BLOCKS.md', 'VERIFY_CHECKLIST.md', 'validation-curl.sh')
SITE_PATHS = ('/agents.json', '/llms.txt', '/.well-known/mcp.json',
              '/.well-known/wever-labs-mcp.json', '/openapi.json',
              '/x402-index/index.json', '/api/agent-operating-products')
MAX_BYTES = 2 * 1024 * 1024
MAX_PAGES = 20
MAX_TOOLS = 1000


class DriftError(Exception):
    """A missing, changed or unavailable discovery contract."""


def require(condition, message):
    if not condition:
        raise DriftError(message)


def decode_json(text, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f'{label}: duplicate JSON key {key}')
            result[key] = value
        return result
    def constant(value):
        raise DriftError(f'{label}: invalid JSON constant {value}')
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, TypeError) as error:
        raise DriftError(f'{label}: invalid JSON ({error})') from error


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise DriftError(f'{req.full_url}: unexpected HTTP redirect {code}')


def fetch_text(url, payload=None):
    headers = {'User-Agent': 'Wever-Catalog-Drift-Check/1.0', 'Cache-Control': 'no-cache'}
    body = None
    if payload is not None:
        headers.update({'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
                        'MCP-Protocol-Version': '2025-03-26'})
        body = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
            require(response.status == 200, f'{url}: HTTP {response.status}')
            if payload is not None:
                require(response.headers.get_content_type() == 'application/json',
                        f'{url}: expected stateless JSON MCP response')
            data = response.read(MAX_BYTES + 1)
            require(len(data) <= MAX_BYTES, f'{url}: response exceeds {MAX_BYTES} bytes')
            return data.decode('utf-8')
    except (OSError, UnicodeError, urllib.error.URLError) as error:
        raise DriftError(f'{url}: discovery unavailable ({error})') from error


def request_json(url, payload):
    return decode_json(fetch_text(url, payload), url)


def validate_tools(tools, label):
    require(isinstance(tools, list) and 0 < len(tools) <= MAX_TOOLS,
            f'{label}: expected 1..{MAX_TOOLS} tool definitions')
    names = []
    for index, tool in enumerate(tools):
        require(isinstance(tool, dict), f'{label}[{index}]: invalid tool')
        name = tool.get('name')
        require(isinstance(name, str) and 0 < len(name) <= 256, f'{label}[{index}]: invalid name')
        require(isinstance(tool.get('inputSchema'), dict) and tool['inputSchema'].get('type') == 'object',
                f'{label}[{index}]: missing object inputSchema')
        require(name not in names, f'{label}: duplicate tool name {name}')
        names.append(name)
    return names


def collect_tools(endpoint, request=request_json):
    """Collect every page from the documented stateless JSON entrance."""
    tools, cursors = [], set()
    cursor = None
    for page in range(1, MAX_PAGES + 1):
        message = request(endpoint, {'jsonrpc': '2.0', 'id': page, 'method': 'tools/list',
                                     'params': {} if cursor is None else {'cursor': cursor}})
        require(isinstance(message, dict) and message.get('jsonrpc') == '2.0'
                and type(message.get('id')) is int and message['id'] == page
                and 'error' not in message, f'{endpoint}: invalid JSON-RPC response on page {page}')
        result = message.get('result')
        require(isinstance(result, dict) and isinstance(result.get('tools'), list),
                f'{endpoint}: missing tools list on page {page}')
        tools.extend(result['tools'])
        validate_tools(tools, endpoint)
        if 'nextCursor' not in result:
            return tools
        cursor = result['nextCursor']
        require(isinstance(cursor, str) and 0 < len(cursor) <= 4096 and cursor not in cursors,
                f'{endpoint}: invalid or repeated pagination cursor')
        cursors.add(cursor)
    raise DriftError(f'{endpoint}: pagination exceeds {MAX_PAGES} pages')


def first_difference(actual, expected, path):
    if type(actual) is not type(expected):
        return path + ' (type)'
    if isinstance(actual, dict):
        if actual.keys() != expected.keys():
            return path + ' (fields)'
        for key in expected:
            difference = first_difference(actual[key], expected[key], f'{path}.{key}')
            if difference:
                return difference
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            return path + ' (length)'
        for index, value in enumerate(expected):
            difference = first_difference(actual[index], value, f'{path}[{index}]')
            if difference:
                return difference
    elif actual != expected:
        return path
    return None


class Checks:
    def __init__(self):
        self.checked = []

    def equal(self, actual, expected, label):
        difference = first_difference(actual, expected, label)
        require(difference is None, f'{difference}: differs from live catalog; expected {expected!r}'
                if isinstance(expected, (int, str)) else f'{difference}: differs from live catalog')
        self.checked.append(label)

    def counts(self, text, pattern, expected, occurrences, label):
        require(isinstance(text, str), f'{label}: expected text claim')
        matches = re.findall(pattern, text, re.MULTILINE)
        require(len(matches) == occurrences,
                f'{label}: expected {occurrences} count claims, found {len(matches)}')
        for index, value in enumerate(matches):
            self.equal(int(value), expected, f'{label}[{index}]')


def check_registry(files, tools, free_count, checks, label='local'):
    total = len(tools)
    for name in REGISTRY_FILES:
        require(name in files, f'{label}/{name}: missing file')
    for name in ('server.json', 'server.dns-auth.example.json', 'lhm.plugin.json'):
        data = decode_json(files[name], f'{label}/{name}')
        checks.counts(data['description'], r'(\d+) production tools', total, 1, f'{label}/{name}:description')
        if name == 'lhm.plugin.json':
            checks.equal(data['cloudEndpoint'], MAIN, f'{label}/{name}:cloudEndpoint')
            validate_tools(data['tools'], f'{label}/{name}:tools')
            checks.equal(data['tools'], tools, f'{label}/{name}:tools')
            checks.counts(data['description'], r'provides (\d+) tools', free_count, 1, f'{label}/{name}:free')
    readme = files['README.md']
    checks.counts(readme, r'(\d+) production tools', total, 1, f'{label}/README.md:intro')
    checks.counts(readme, r'^\| Production tools \| (\d+) \|$', total, 1, f'{label}/README.md:table')
    checks.counts(readme, r'current (\d+)-tool server', total, 1, f'{label}/README.md:current')
    checks.counts(readme, r'(\d+) tools', free_count, 2, f'{label}/README.md:free')
    checks.counts(files['REGISTRY_COPY_BLOCKS.md'], r'(\d+) production(?: MCP)? tools', total, 3,
                  f'{label}/REGISTRY_COPY_BLOCKS.md:main')
    checks.counts(files['REGISTRY_COPY_BLOCKS.md'], r'has (\d+) tools', free_count, 1,
                  f'{label}/REGISTRY_COPY_BLOCKS.md:free')
    checklist = files['VERIFY_CHECKLIST.md']
    checks.counts(checklist, r'(\d+) production tools', total, 2, f'{label}/VERIFY_CHECKLIST.md:main')
    checks.counts(checklist, r'(\d+)/\d+ tool counts', total, 1, f'{label}/VERIFY_CHECKLIST.md:pair-main')
    checks.counts(checklist, r'\d+/(\d+) tool counts', free_count, 1, f'{label}/VERIFY_CHECKLIST.md:pair-free')
    checks.counts(checklist, r'lists (\d+) tools without', free_count, 1, f'{label}/VERIFY_CHECKLIST.md:free')
    expected = re.findall(r'^\s*expected_count=(\d+)$', files['validation-curl.sh'], re.MULTILINE)
    checks.equal([int(value) for value in expected], [total, free_count], f'{label}/validation-curl.sh:counts')
    # DIRECTORY_STATUS and CURSOR_MARKETPLACE are explicitly dated observations.


def one(items, predicate, label):
    matches = [item for item in items if predicate(item)]
    require(len(matches) == 1, f'{label}: expected exactly one main endpoint entry')
    return matches[0]


def check_site(site, tools, checks):
    names = [tool['name'] for tool in tools]
    total = len(names)
    products = site['/api/agent-operating-products']
    keys = [product['key'] for product in products['products']]
    require(keys and len(set(keys)) == len(keys), 'product catalog: empty or duplicate product keys')
    require(all('wever_' + key in names for key in keys), 'product catalog: product missing from live tools')
    product_count = len(keys)
    checks.equal(products['count'], product_count, 'product catalog:count')
    agents = site['/agents.json']
    checks.equal(agents['machine_readable']['production_mcp_tool_count'], total, 'agents.json:main_count')
    checks.equal(agents['machine_readable']['product_count'], product_count, 'agents.json:product_count')
    operating = agents['agent_operating_products_v1']
    checks.equal(operating['count'], product_count, 'agents.json:operating_count')
    checks.equal([product['key'] for product in operating['products']], keys, 'agents.json:product_keys')
    checks.counts(operating['scope'], r'Its (\d+) product identities', product_count, 1, 'agents.json:product_scope')
    paid = agents['current_paid_production_tools']
    paid_names = [tool['mcp_name'] for tool in paid['tools']]
    require(paid_names and len(paid_names) == len(set(paid_names)) and set(paid_names) <= set(names),
            'agents.json: priced tools must be unique live tools')
    checks.equal(paid['tool_count'], len(paid_names), 'agents.json:priced_count')
    checks.equal(paid['product_count'], product_count, 'agents.json:paid_product_count')
    checks.counts(paid['boundary'], r'The (\d+) priced tools', len(paid_names), 1, 'agents.json:priced_boundary')
    checks.counts(paid['daily_brief_scope'], r'This list contains (\d+) priced MCP tools', len(paid_names), 1, 'agents.json:priced_scope')
    checks.counts(paid['daily_brief_scope'], r'main endpoint declares (\d+) tools', total, 1, 'agents.json:main_scope')
    checks.counts(paid['daily_brief_scope'], r'catalog retains (\d+) products', product_count, 1, 'agents.json:product_scope_total')
    llms = site['/llms.txt']
    checks.counts(llms, r'^MCP catalog: (\d+) tools:', total, 1, 'llms.txt:main_count')
    checks.counts(llms, r'infrastructure with (\d+) production tools', len(paid_names), 1, 'llms.txt:priced_intro')
    checks.counts(llms, r'^MCP catalog: \d+ tools: (\d+) production tools', len(paid_names), 1, 'llms.txt:priced_count')
    checks.counts(llms, r'^Product catalog: .*\((\d+) products;', product_count, 1, 'llms.txt:product_count')
    line = one(llms.splitlines(), lambda line: line.startswith('MCP catalog:'), 'llms.txt:catalog line')
    read_names = set(names) & {'wever_boutique-list-products', 'wever_boutique-product-detail'}
    # These are the current catalog categories. A new category needs an explicit
    # classification here, so an unknown declaration cannot silently fill a gap.
    groups = {
        'production tools': set(paid_names),
        'free boutique catalog reads': read_names,
        'boutique checkout simulation and acceptance tools': {
            name for name in names if name.startswith('wever_boutique-')} - read_names,
        'agent purchase tools': {name for name in names if name.startswith('wever_purchase-')},
    }
    if 'edge-alert' in names:
        groups['free Edge Alert tool'] = {'edge-alert'}
    if 'boutique-coupon' in names:
        groups['free boutique coupon tool'] = {'boutique-coupon'}
    require(sum(map(len, groups.values())) == len(set().union(*groups.values())),
            'llms.txt: overlapping tool categories')
    checks.equal(sorted(set().union(*groups.values())), sorted(names), 'llms.txt:category_coverage')
    for category, group in groups.items():
        checks.counts(line, r'(\d+) ' + re.escape(category), len(group), 1, f'llms.txt:{category}')
    checks.counts(line, r'(\d+) demo labels', 0, 1, 'llms.txt:demo_count')
    descriptor = one(site['/.well-known/mcp.json']['servers'],
                     lambda item: item.get('transport', {}).get('url') == MAIN, 'mcp.json')
    detailed = site['/.well-known/wever-labs-mcp.json']
    for label, data in (('mcp.json', descriptor), ('wever-labs-mcp.json', detailed)):
        for field in ('toolCount', 'productionToolCount'):
            checks.equal(data[field], total, f'{label}:{field}')
        checks.equal(data['productCount'], product_count, f'{label}:productCount')
    checks.counts(detailed['description'], r'MCP access to (\d+) Wever Labs product adapters', product_count, 1, 'wever-labs-mcp.json:product_description')
    checks.counts(detailed['description'], r'main /mcp endpoint declares (\d+) tools', total, 1, 'wever-labs-mcp.json:main_description')
    checks.counts(detailed['description'], r'(\d+) priced tools advertise', len(paid_names), 1, 'wever-labs-mcp.json:priced_description')
    checks.counts(detailed['availability'], r'main MCP endpoint declares (\d+) tools', total, 1, 'wever-labs-mcp.json:availability_count')
    checks.counts(detailed['availability'], r'Its (\d+) priced tools', len(paid_names), 1, 'wever-labs-mcp.json:availability_priced')
    checks.counts(detailed['dailyBrief']['scope'], r'current (\d+)-tool MCP surface', total, 1, 'wever-labs-mcp.json:brief_main_count')
    checks.counts(detailed['dailyBrief']['scope'], r'catalog retains (\d+) products', product_count, 1, 'wever-labs-mcp.json:brief_products')
    openapi = site['/openapi.json']
    discovery = openapi['x-wever-current-production-discovery']
    checks.equal(discovery['tool_count'], total, 'openapi.json:main_count')
    checks.equal(discovery['tools'], names, 'openapi.json:tool_names')
    checks.equal(discovery['product_count'], product_count, 'openapi.json:product_count')
    route = openapi['paths']['/mcp']['post']
    checks.equal(route['x-mcp-tools'], names, 'openapi.json:route_tools')
    checks.counts(route['summary'], r'(\d+)-tool Wever production MCP endpoint', total, 1, 'openapi.json:summary')
    checks.counts(route['description'], r'this (\d+)-tool endpoint', total, 1, 'openapi.json:description')
    product_route = openapi['paths']['/api/agent-operating-products']['get']
    checks.counts(product_route['summary'], r'current (\d+)-product catalog', product_count, 1, 'openapi.json:product_summary')
    checks.counts(product_route['description'], r'catalog contains (\d+) products', product_count, 1, 'openapi.json:product_description')
    response = product_route['responses']['200']
    checks.counts(response['description'], r'exactly (\d+) products', product_count, 1, 'openapi.json:product_response')
    properties = response['content']['application/json']['schema']['properties']
    checks.equal(properties['count']['const'], product_count, 'openapi.json:product_const')
    for field in ('minItems', 'maxItems'):
        checks.equal(properties['products'][field], product_count, f'openapi.json:products.{field}')
    index = one(site['/x402-index/index.json']['endpoints'], lambda item: item.get('url') == MAIN, 'x402 index')
    checks.equal(index['tool_count'], total, 'x402 index:tool_count')
    return product_count, len(paid_names)


def audit(local, site, tools, free_tools, published=None):
    try:
        validate_tools(tools, 'live /mcp')
        validate_tools(free_tools, 'live /mcp-free')
        checks = Checks()
        check_registry(local, tools, len(free_tools), checks)
        if published is not None:
            check_registry(published, tools, len(free_tools), checks, 'published')
        products, priced = check_site(site, tools, checks)
        return {'status': 'passed', 'main_tools': len(tools), 'free_tools': len(free_tools),
                'products': products, 'priced_tools': priced, 'checks': len(checks.checked),
                'published_registry_checked': published is not None, 'surfaces': checks.checked}
    except (KeyError, IndexError, TypeError, AttributeError) as error:
        raise DriftError(f'missing or malformed discovery field: {error}') from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--published', action='store_true', help='also check public registry main files')
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        tools = collect_tools(MAIN)
        free_tools = collect_tools(FREE)
        local = {name: (root / name).read_text(encoding='utf-8') for name in REGISTRY_FILES}
        site = {}
        for path in SITE_PATHS:
            text = fetch_text(ORIGIN + path)
            site[path] = text if path.endswith('.txt') else decode_json(text, path)
        published = None
        if args.published:
            published = {name: fetch_text(PUBLIC_REGISTRY + name) for name in REGISTRY_FILES}
        print(json.dumps(audit(local, site, tools, free_tools, published), indent=2))
        return 0
    except (DriftError, OSError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
