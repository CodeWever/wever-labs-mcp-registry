"""Offline regression coverage for discovery count and complete catalog drift."""
import contextlib
import copy
from email.message import Message
import importlib.util
import io
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import urllib.error

SPEC = importlib.util.spec_from_file_location(
    'catalog_drift', Path(__file__).resolve().parents[1] / 'scripts/check_catalog_drift.py')
drift = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(drift)


def fixture(total=57, products=29, priced=None, free=6, edge_alert=False, boutique_coupon=False):
    """Keep categories distinct while allowing a fully aligned live count change."""
    priced = total - 10 - int(edge_alert) - int(boutique_coupon) if priced is None else priced
    tools = [{
        'name': f'wever_product-{index}', 'description': f'Tool {index}',
        'inputSchema': {'type': 'object', 'properties': {
            'value': {'type': 'integer', 'minimum': 1}}, 'additionalProperties': False},
        'annotations': {'readOnlyHint': True},
    } for index in range(total)]
    unpriced_names = [
        'wever_boutique-list-products', 'wever_boutique-product-detail',
        'wever_boutique-create-order', 'wever_boutique-record-shipment',
        'wever_boutique-confirm-delivery', 'wever_boutique-real-money-acceptance',
        'wever_purchase-create-intent', 'wever_purchase-status',
        'wever_purchase-execute', 'wever_purchase-dispute',
    ]
    if edge_alert:
        unpriced_names.append('edge-alert')
    if boutique_coupon:
        unpriced_names.append('boutique-coupon')
    for tool, name in zip(tools[priced:], unpriced_names):
        tool['name'] = name
    free_tools = [{**copy.deepcopy(tools[index]), 'name': f'wever_free-{index}'}
                  for index in range(free)]
    keys = [f'product-{index}' for index in range(products)]
    product_list = [{'key': key} for key in keys]
    names = [tool['name'] for tool in tools]
    description = f'{total} production tools. Free entry provides {free} tools.'
    registry = {
        'server.json': json.dumps({'description': description}),
        'server.dns-auth.example.json': json.dumps({'description': description}),
        'lhm.plugin.json': json.dumps({'description': description,
                                      'cloudEndpoint': drift.MAIN, 'tools': tools}),
        'README.md': (f'{total} production tools\n| Production tools | {total} |\n'
                      f'current {total}-tool server\nFree entry: {free} tools\n'
                      f'Index: {free} tools\nHistorical discovery: 33; old snapshot: 20.\n'),
        'REGISTRY_COPY_BLOCKS.md': (f'{total} production tools\n{total} production MCP tools\n'
                                    f'{total} production tools\nFree entry has {free} tools\n'),
        'VERIFY_CHECKLIST.md': (f'{total} production tools\n{total} production tools\n'
                                f'{total}/{free} tool counts\nlists {free} tools without payment\n'),
        'validation-curl.sh': f'  expected_count={total}\n  expected_count={free}\n',
        'DIRECTORY_STATUS.md': 'Dated observation: 33 tools.\n',
        'CURSOR_MARKETPLACE.md': 'Dated observation: 20 tools.\n',
    }
    detailed = {
        'toolCount': total, 'productionToolCount': total, 'productCount': products,
        'description': (f'MCP access to {products} Wever Labs product adapters; '
                        f'main /mcp endpoint declares {total} tools; '
                        f'{priced} priced tools advertise terms'),
        'availability': (f'main MCP endpoint declares {total} tools. '
                         f'Its {priced} priced tools are listed.'),
        'dailyBrief': {'scope': (f'current {total}-tool MCP surface; '
                                f'catalog retains {products} products')},
    }
    site = {
        '/api/agent-operating-products': {'count': products, 'products': product_list},
        '/agents.json': {
            'machine_readable': {'production_mcp_tool_count': total, 'product_count': products},
            'agent_operating_products_v1': {
                'count': products, 'products': copy.deepcopy(product_list),
                'scope': f'Its {products} product identities are listed'},
            'current_paid_production_tools': {
                'tools': [{'mcp_name': name} for name in names[:priced]],
                'tool_count': priced, 'product_count': products,
                'boundary': f'The {priced} priced tools have declared terms',
                'daily_brief_scope': (f'This list contains {priced} priced MCP tools; '
                                      f'main endpoint declares {total} tools; '
                                      f'catalog retains {products} products')},
        },
        '/llms.txt': (f'Agent infrastructure with {priced} production tools\n'
                      f'MCP catalog: {total} tools: {priced} production tools, '
                      '2 free boutique catalog reads, '
                      '4 boutique checkout simulation and acceptance tools, 4 agent purchase tools, 0 demo labels\n'
                      f'Product catalog: products ({products} products; listed)\n'),
        '/.well-known/mcp.json': {'servers': [
            {'transport': {'url': drift.FREE}, 'toolCount': free},
            {'transport': {'url': drift.MAIN}, 'toolCount': total,
             'productionToolCount': total, 'productCount': products}]},
        '/.well-known/wever-labs-mcp.json': detailed,
        '/openapi.json': {
            'x-wever-current-production-discovery': {
                'tool_count': total, 'tools': names, 'product_count': products},
            'paths': {
                '/mcp': {'post': {
                    'x-mcp-tools': list(names),
                    'summary': f'{total}-tool Wever production MCP endpoint',
                    'description': f'Use this {total}-tool endpoint'}},
                '/api/agent-operating-products': {'get': {
                    'summary': f'The current {products}-product catalog',
                    'description': f'The catalog contains {products} products',
                    'responses': {'200': {
                        'description': f'Returns exactly {products} products',
                        'content': {'application/json': {'schema': {'properties': {
                            'count': {'const': products},
                            'products': {'minItems': products, 'maxItems': products},
                        }}}},
                    }},
                }},
            },
        },
        '/x402-index/index.json': {'endpoints': [
            {'url': drift.MAIN, 'tool_count': total},
            {'url': drift.FREE, 'tool_count': free}]},
    }
    if edge_alert:
        site['/llms.txt'] = site['/llms.txt'].replace('4 agent purchase tools, 0 demo labels', '4 agent purchase tools, 1 free Edge Alert tool, 0 demo labels')
    if boutique_coupon:
        site['/llms.txt'] = site['/llms.txt'].replace('2 free boutique catalog reads, ', '2 free boutique catalog reads, 1 free boutique coupon tool, ')
    return registry, site, tools, free_tools


def numeric_locations(value, path=()):
    """Find numeric fields without treating booleans as integer counts."""
    if type(value) is int:
        yield path
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from numeric_locations(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from numeric_locations(child, (*path, index))


def replace_at(value, path, replacement):
    for key in path[:-1]:
        value = value[key]
    value[path[-1]] = replacement


class CatalogAuditTests(unittest.TestCase):
    def test_free_edge_alert_has_its_own_category_and_keeps_priced_count(self):
        registry, site, tools, free_tools = fixture(71, priced=60, edge_alert=True)
        result = drift.audit(registry, site, tools, free_tools)
        self.assertEqual(result['main_tools'], 71)
        self.assertEqual(result['priced_tools'], 60)
        self.assertEqual(result['free_tools'], 6)
        site['/llms.txt'] = site['/llms.txt'].replace('1 free Edge Alert tool', '2 free Edge Alert tool')
        with self.assertRaises(drift.DriftError):
            drift.audit(registry, site, tools, free_tools)

    def test_free_coupon_and_edge_alert_have_distinct_categories_and_keep_pricing(self):
        registry, site, tools, free_tools = fixture(72, priced=60, edge_alert=True, boutique_coupon=True)
        result = drift.audit(registry, site, tools, free_tools)
        self.assertEqual((result['main_tools'], result['priced_tools'], result['free_tools']), (72, 60, 6))
        self.assertIn('llms.txt:free boutique coupon tool[0]', result['surfaces'])
        self.assertIn('llms.txt:free Edge Alert tool[0]', result['surfaces'])
        baseline = site['/llms.txt']
        mutations = [
            baseline.replace('1 free boutique coupon tool', '2 free boutique coupon tool'),
            baseline.replace('1 free boutique coupon tool, ', ''),
            baseline.replace('1 free boutique coupon tool', '2 free boutique coupon tool').replace(
                '1 free Edge Alert tool', '0 free Edge Alert tool'),
        ]
        for text in mutations:
            with self.subTest(text=text):
                site['/llms.txt'] = text
                with self.assertRaises(drift.DriftError):
                    drift.audit(registry, site, tools, free_tools)

    def setUp(self):
        self.registry, self.site, self.tools, self.free_tools = fixture()

    def audit(self, **overrides):
        return drift.audit(overrides.get('registry', self.registry),
                           overrides.get('site', self.site),
                           overrides.get('tools', self.tools),
                           overrides.get('free_tools', self.free_tools),
                           overrides.get('published'))

    def edit_plugin(self, edit):
        plugin = json.loads(self.registry['lhm.plugin.json'])
        edit(plugin)
        self.registry['lhm.plugin.json'] = json.dumps(plugin)

    def test_aligned_57_and_future_58_are_derived_from_live_catalog(self):
        for total in [57, 58]:
            with self.subTest(total=total):
                registry, site, tools, free_tools = fixture(total=total)
                report = drift.audit(registry, site, tools, free_tools)
                self.assertEqual(report['status'], 'passed')
                self.assertEqual(report['main_tools'], total)
                self.assertEqual(report['free_tools'], 6)
                self.assertEqual(report['products'], 29)
                self.assertEqual(report['priced_tools'], total - 10)
                self.assertFalse(report['published_registry_checked'])
                self.assertGreater(report['checks'], 50)

    def test_each_registry_count_claim_rejects_stale_value(self):
        for name in drift.REGISTRY_FILES:
            if name.endswith('.json'):
                data = json.loads(self.registry[name])
                text = data['description']
                matches = list(re.finditer(r'\d+', text))
                if name != 'lhm.plugin.json':
                    matches = matches[:1]
                for match in matches:
                    with self.subTest(file=name, count=match.group()):
                        altered = copy.deepcopy(data)
                        altered['description'] = text[:match.start()] + '999' + text[match.end():]
                        registry = dict(self.registry, **{name: json.dumps(altered)})
                        with self.assertRaises(drift.DriftError):
                            self.audit(registry=registry)
            else:
                text = self.registry[name]
                for match in re.finditer(r'\d+', text):
                    if match.group() in ('33', '20'):
                        continue
                    with self.subTest(file=name, offset=match.start()):
                        registry = dict(self.registry)
                        registry[name] = text[:match.start()] + '999' + text[match.end():]
                        with self.assertRaises(drift.DriftError):
                            self.audit(registry=registry)

    def test_each_site_numeric_count_rejects_stale_value(self):
        for path in numeric_locations(self.site):
            if path in [('/.well-known/mcp.json', 'servers', 0, 'toolCount'),
                        ('/x402-index/index.json', 'endpoints', 1, 'tool_count')]:
                continue  # Those entries describe the separate free entrance.
            with self.subTest(path=path):
                site = copy.deepcopy(self.site)
                replace_at(site, path, 999)
                with self.assertRaises(drift.DriftError):
                    self.audit(site=site)

    def test_each_site_text_count_rejects_stale_value(self):
        paths = [
            ('/agents.json', 'agent_operating_products_v1', 'scope'),
            ('/agents.json', 'current_paid_production_tools', 'boundary'),
            ('/agents.json', 'current_paid_production_tools', 'daily_brief_scope'),
            ('/llms.txt',),
            ('/.well-known/wever-labs-mcp.json', 'description'),
            ('/.well-known/wever-labs-mcp.json', 'availability'),
            ('/.well-known/wever-labs-mcp.json', 'dailyBrief', 'scope'),
            ('/openapi.json', 'paths', '/mcp', 'post', 'summary'),
            ('/openapi.json', 'paths', '/mcp', 'post', 'description'),
            ('/openapi.json', 'paths', '/api/agent-operating-products', 'get', 'summary'),
            ('/openapi.json', 'paths', '/api/agent-operating-products', 'get', 'description'),
            ('/openapi.json', 'paths', '/api/agent-operating-products', 'get', 'responses', '200', 'description'),
        ]
        for path in paths:
            text = self.site
            for key in path:
                text = text[key]
            for match in re.finditer(r'\d+', text):
                with self.subTest(path=path, offset=match.start()):
                    site = copy.deepcopy(self.site)
                    replace_at(site, path, text[:match.start()] + '999' + text[match.end():])
                    with self.assertRaises(drift.DriftError):
                        self.audit(site=site)

    def test_same_count_live_rename_is_detected(self):
        self.tools[-1]['name'] = 'wever_renamed'
        with self.assertRaisesRegex(drift.DriftError, 'tools\\[56\\].name'):
            self.audit()

    def test_missing_extra_and_reordered_embedded_definitions_are_detected(self):
        edits = {
            'missing': lambda tools: tools.pop(),
            'extra': lambda tools: tools.append({**copy.deepcopy(tools[0]), 'name': 'wever_extra'}),
            'reordered': lambda tools: tools.reverse(),
        }
        for label, edit in edits.items():
            with self.subTest(edit=label):
                registry = copy.deepcopy(self.registry)
                plugin = json.loads(registry['lhm.plugin.json'])
                edit(plugin['tools'])
                registry['lhm.plugin.json'] = json.dumps(plugin)
                with self.assertRaises(drift.DriftError):
                    self.audit(registry=registry)

    def test_complete_definition_fields_and_types_are_compared(self):
        edits = {
            'description': lambda tool: tool.update(description='Changed'),
            'schema': lambda tool: tool['inputSchema']['properties']['value'].update(minimum=2),
            'annotations': lambda tool: tool['annotations'].update(readOnlyHint=False),
            'boolean_integer': lambda tool: tool['annotations'].update(readOnlyHint=1),
            'integer_float': lambda tool: tool['inputSchema']['properties']['value'].update(minimum=1.0),
            'extra_field': lambda tool: tool.update(title='Added title'),
            'missing_field': lambda tool: tool.pop('description'),
        }
        for label, edit in edits.items():
            with self.subTest(edit=label):
                registry = copy.deepcopy(self.registry)
                plugin = json.loads(registry['lhm.plugin.json'])
                edit(plugin['tools'][0])
                registry['lhm.plugin.json'] = json.dumps(plugin)
                with self.assertRaises(drift.DriftError):
                    self.audit(registry=registry)

    def test_object_key_order_and_non_contract_copy_do_not_cause_drift(self):
        self.edit_plugin(lambda plugin: plugin['tools'].__setitem__(
            0, dict(reversed(list(plugin['tools'][0].items())))))
        self.registry['README.md'] += 'Additional prose with no count claim.\n'
        self.assertEqual(self.audit()['status'], 'passed')

    def test_duplicate_or_malformed_live_and_embedded_tools_are_rejected(self):
        invalid = [[], {}, [None], [{'name': ''}],
                   [{'name': 'wever_invalid', 'inputSchema': {'type': 'array'}}],
                   [self.tools[0], self.tools[0]]]
        for tools in invalid:
            for source in ('live', 'embedded'):
                with self.subTest(source=source, tools=tools):
                    registry = dict(self.registry)
                    if source == 'embedded':
                        plugin = json.loads(registry['lhm.plugin.json'])
                        plugin['tools'] = tools
                        registry['lhm.plugin.json'] = json.dumps(plugin)
                    with self.assertRaises(drift.DriftError):
                        self.audit(registry=registry, tools=tools if source == 'live' else self.tools)

    def test_missing_claims_files_or_fields_are_rejected(self):
        registry = dict(self.registry)
        registry['README.md'] = registry['README.md'].replace('57 production tools', 'Production tools')
        with self.assertRaises(drift.DriftError):
            self.audit(registry=registry)
        for name in drift.REGISTRY_FILES:
            with self.subTest(missing=name):
                registry = dict(self.registry)
                registry.pop(name)
                with self.assertRaises(drift.DriftError):
                    self.audit(registry=registry)
        for name in drift.SITE_PATHS:
            with self.subTest(missing=name):
                site = dict(self.site)
                site.pop(name)
                with self.assertRaises(drift.DriftError):
                    self.audit(site=site)

    def test_product_priced_and_historical_counts_remain_distinct(self):
        self.registry['DIRECTORY_STATUS.md'] = 'Historical 33 tools and 20 tools.'
        self.registry['CURSOR_MARKETPLACE.md'] = 'Historical 20 tools and 33 tools.'
        report = self.audit()
        self.assertEqual((report['main_tools'], report['products'], report['priced_tools']), (57, 29, 47))
        self.site['/agents.json']['current_paid_production_tools']['tool_count'] = 57
        with self.assertRaises(drift.DriftError):
            self.audit()

    def test_equal_offset_category_counts_and_demo_count_are_rejected(self):
        baseline = self.site['/llms.txt']
        mutations = [
            baseline.replace('2 free boutique catalog reads', '3 free boutique catalog reads').replace(
                '4 boutique checkout simulation and acceptance tools',
                '3 boutique checkout simulation and acceptance tools'),
            baseline.replace('0 demo labels', '1 demo labels'),
            baseline.replace(', 0 demo labels', ''),
        ]
        for text in mutations:
            with self.subTest(text=text):
                site = copy.deepcopy(self.site)
                site['/llms.txt'] = text
                with self.assertRaises(drift.DriftError):
                    self.audit(site=site)

    def test_product_and_priced_lists_require_unique_live_membership(self):
        for section, field in [('products', 'key'), ('priced', 'mcp_name')]:
            for failure in ['duplicate', 'unknown', 'empty']:
                with self.subTest(section=section, failure=failure):
                    site = copy.deepcopy(self.site)
                    items = (site['/api/agent-operating-products']['products'] if section == 'products'
                             else site['/agents.json']['current_paid_production_tools']['tools'])
                    if failure == 'duplicate':
                        items[-1] = copy.deepcopy(items[0])
                    elif failure == 'unknown':
                        items[-1][field] = 'unknown'
                    else:
                        items.clear()
                    with self.assertRaises(drift.DriftError):
                        self.audit(site=site)

    def test_openapi_same_count_names_and_order_are_checked(self):
        for path in [('/openapi.json', 'x-wever-current-production-discovery', 'tools'),
                     ('/openapi.json', 'paths', '/mcp', 'post', 'x-mcp-tools')]:
            with self.subTest(path=path):
                site = copy.deepcopy(self.site)
                replace_at(site, path, list(reversed([tool['name'] for tool in self.tools])))
                with self.assertRaises(drift.DriftError):
                    self.audit(site=site)

    def test_main_endpoint_entries_must_be_unique_and_well_formed(self):
        for path, entries in [('/.well-known/mcp.json', 'servers'), ('/x402-index/index.json', 'endpoints')]:
            for replacement in [[], ['invalid'], [None]]:
                with self.subTest(path=path, replacement=replacement):
                    site = copy.deepcopy(self.site)
                    site[path][entries] = replacement
                    with self.assertRaises(drift.DriftError):
                        self.audit(site=site)
            site = copy.deepcopy(self.site)
            site[path][entries] *= 2
            with self.assertRaises(drift.DriftError):
                self.audit(site=site)

    def test_published_registry_is_checked_independently(self):
        published = copy.deepcopy(self.registry)
        self.assertTrue(self.audit(published=published)['published_registry_checked'])
        published['server.json'] = published['server.json'].replace('57 production', '56 production')
        with self.assertRaisesRegex(drift.DriftError, 'published/server.json'):
            self.audit(published=published)
        published = copy.deepcopy(self.registry)
        plugin = json.loads(published['lhm.plugin.json'])
        plugin['tools'][0]['description'] = 'Stale public definition'
        published['lhm.plugin.json'] = json.dumps(plugin)
        with self.assertRaisesRegex(drift.DriftError, 'published/lhm.plugin.json'):
            self.audit(published=published)

    def test_audit_is_read_only(self):
        before = copy.deepcopy((self.registry, self.site, self.tools, self.free_tools))
        self.audit(published=copy.deepcopy(self.registry))
        self.assertEqual(before, (self.registry, self.site, self.tools, self.free_tools))


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tools = fixture()[2]

    def test_pagination_collects_every_tool_and_sends_only_tools_list(self):
        requests = []
        def request(endpoint, payload):
            requests.append((endpoint, payload))
            if len(requests) == 1:
                return {'jsonrpc': '2.0', 'id': 1, 'result': {'tools': self.tools[:25], 'nextCursor': 'page2'}}
            return {'jsonrpc': '2.0', 'id': 2, 'result': {'tools': self.tools[25:]}}
        self.assertEqual(drift.collect_tools(drift.MAIN, request), self.tools)
        self.assertEqual(requests, [
            (drift.MAIN, {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list', 'params': {}}),
            (drift.MAIN, {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {'cursor': 'page2'}}),
        ])

    def test_jsonrpc_error_wrong_identity_and_malformed_result_are_rejected(self):
        valid = {'jsonrpc': '2.0', 'id': 1, 'result': {'tools': self.tools}}
        messages = [None, [], {}, {**valid, 'error': {'code': -32603}},
                    {**valid, 'jsonrpc': '1.0'}, {**valid, 'id': 2}, {**valid, 'id': True},
                    {**valid, 'id': '1'}, {**valid, 'result': {}},
                    {**valid, 'result': {'tools': {}}}, {**valid, 'result': {'tools': []}}]
        for message in messages:
            with self.subTest(message=message):
                with self.assertRaises(drift.DriftError):
                    drift.collect_tools(drift.MAIN, lambda *_: message)

    def test_invalid_repeated_and_unbounded_cursors_are_rejected(self):
        for cursor in [None, '', True, 2, {}, 'x' * 4097]:
            with self.subTest(cursor=cursor):
                with self.assertRaises(drift.DriftError):
                    drift.collect_tools(drift.MAIN, lambda *_: {
                        'jsonrpc': '2.0', 'id': 1,
                        'result': {'tools': self.tools[:1], 'nextCursor': cursor}})
        def repeating(endpoint, payload):
            page = payload['id']
            return {'jsonrpc': '2.0', 'id': page,
                    'result': {'tools': self.tools[page - 1:page], 'nextCursor': 'same'}}
        with self.assertRaisesRegex(drift.DriftError, 'repeated pagination cursor'):
            drift.collect_tools(drift.MAIN, repeating)
        def endless(endpoint, payload):
            page = payload['id']
            return {'jsonrpc': '2.0', 'id': page,
                    'result': {'tools': self.tools[page - 1:page], 'nextCursor': str(page)}}
        with self.assertRaisesRegex(drift.DriftError, 'pagination exceeds'):
            drift.collect_tools(drift.MAIN, endless)

    def test_duplicate_across_pages_and_tool_limit_are_rejected(self):
        def duplicate(endpoint, payload):
            result = {'tools': self.tools[:1]}
            if payload['id'] == 1:
                result['nextCursor'] = 'next'
            return {'jsonrpc': '2.0', 'id': payload['id'], 'result': result}
        with self.assertRaisesRegex(drift.DriftError, 'duplicate tool name'):
            drift.collect_tools(drift.MAIN, duplicate)
        with patch.object(drift, 'MAX_TOOLS', 2):
            with self.assertRaises(drift.DriftError):
                drift.collect_tools(drift.MAIN, lambda *_: {
                    'jsonrpc': '2.0', 'id': 1, 'result': {'tools': self.tools[:3]}})

    def test_json_decoder_rejects_duplicate_keys_constants_and_malformed_json(self):
        for text in ['{"a":1,"a":2}', '{"nested":{"x":1,"x":2}}',
                     '{"n":NaN}', '{"n":Infinity}', '{"n":-Infinity}', '{']:
            with self.subTest(text=text):
                with self.assertRaises(drift.DriftError):
                    drift.decode_json(text, 'fixture')
        self.assertEqual(drift.decode_json('{"a":1}', 'fixture'), {'a': 1})

    def test_transport_header_timeout_and_size_bound(self):
        response = Response(b'{"ok":true}')
        opener = unittest.mock.Mock()
        opener.open.return_value = response
        with patch.object(drift.urllib.request, 'build_opener', return_value=opener):
            result = drift.fetch_text(drift.MAIN, {'jsonrpc': '2.0', 'method': 'tools/list'})
        self.assertEqual(result, '{"ok":true}')
        request = opener.open.call_args.args[0]
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(request.get_header('Accept'), 'application/json, text/event-stream')
        self.assertEqual(request.get_header('Content-type'), 'application/json')
        self.assertEqual(request.get_header('Mcp-protocol-version'), '2025-03-26')
        self.assertEqual(opener.open.call_args.kwargs['timeout'], 30)
        self.assertEqual(response.read_limit, drift.MAX_BYTES + 1)

    def test_transport_rejects_status_content_type_size_encoding_and_network_error(self):
        cases = [Response(b'{}', status=500), Response(b'{}', content_type='text/event-stream'),
                 Response(b'\xff'), Response(b'x' * (drift.MAX_BYTES + 1))]
        for response in cases:
            with self.subTest(status=response.status, size=len(response.data)):
                opener = unittest.mock.Mock()
                opener.open.return_value = response
                with patch.object(drift.urllib.request, 'build_opener', return_value=opener):
                    with self.assertRaises(drift.DriftError):
                        drift.fetch_text(drift.MAIN, {'method': 'tools/list'})
        opener = unittest.mock.Mock()
        opener.open.side_effect = urllib.error.URLError('unavailable')
        with patch.object(drift.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaises(drift.DriftError):
                drift.fetch_text(drift.MAIN)

    def test_redirect_is_rejected(self):
        with self.assertRaises(drift.DriftError):
            drift.NoRedirect().redirect_request(
                drift.urllib.request.Request(drift.MAIN), None, 302, 'Found', {}, 'https://elsewhere.invalid')

    def test_cli_reports_success_and_failure_without_network(self):
        registry, site, tools, free_tools = fixture()
        def fetch(url, payload=None):
            if url.startswith(drift.PUBLIC_REGISTRY):
                return registry[url.removeprefix(drift.PUBLIC_REGISTRY)]
            value = site[url.removeprefix(drift.ORIGIN)]
            return value if isinstance(value, str) else json.dumps(value)
        def read_text(path, **kwargs):
            return registry[path.name]
        with patch.object(drift, 'collect_tools', side_effect=[tools, free_tools]), \
                patch.object(drift, 'fetch_text', side_effect=fetch), \
                patch.object(Path, 'read_text', read_text), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(drift.main(['--published']), 0)
        self.assertTrue(json.loads(output.getvalue())['published_registry_checked'])
        with patch.object(drift, 'collect_tools', side_effect=drift.DriftError('unavailable')), \
                contextlib.redirect_stderr(io.StringIO()) as error:
            self.assertEqual(drift.main([]), 1)
        self.assertEqual(json.loads(error.getvalue()), {'status': 'failed', 'error': 'unavailable'})


class Response:
    def __init__(self, data, status=200, content_type='application/json'):
        self.data, self.status = data, status
        self.headers = Message()
        self.headers['Content-Type'] = content_type
        self.read_limit = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit):
        self.read_limit = limit
        return self.data[:limit]


if __name__ == '__main__':
    unittest.main()
