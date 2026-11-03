#!/usr/bin/env python3
"""Offline checks for the Antigravity plugin bundle, plus its live tool reference.

The checks follow https://antigravity.google/docs/build-plugins, the hosted
manifest schema at https://antigravity.google/schemas/v1/plugin.json and the MCP
configuration table at https://antigravity.google/docs/mcp. They do not replace
`agy plugin validate --strict`; run that too before submission.

  python3 scripts/check_antigravity_plugin.py            # offline bundle checks
  python3 scripts/check_antigravity_plugin.py --strict   # warnings count as errors
  python3 scripts/check_antigravity_plugin.py --live     # also compare tool names with live tools/list
  python3 scripts/check_antigravity_plugin.py --write-reference   # regenerate references/tools.md from live
"""
import argparse
import datetime
import json
from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'antigravity' / 'wever-labs'
REFERENCE = Path('skills') / 'wever-labs' / 'references' / 'tools.md'
SCHEMA_URL = 'https://antigravity.google/schemas/v1/plugin.json'

# Top-level keys accepted by the hosted schema (additionalProperties: false).
MANIFEST_KEYS = {'$schema', 'name', 'displayName', 'display_name', 'description', 'version', 'disabled',
                 'logo', 'suggestedPrompts', 'suggested_prompts', 'skills', 'author', 'homepage',
                 'repository', 'license', 'keywords', 'extensions', 'source', 'sourcePath', 'source_path'}
DEPRECATED_KEYS = {'source', 'sourcePath', 'source_path'}
MARKETPLACE_REQUIRED = ('name', 'displayName', 'description', 'version', 'logo', 'suggestedPrompts', 'author')
DOC_NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')          # build-plugins field reference
SCHEMA_NAME = re.compile(r'^[a-zA-Z0-9_-]+$')               # hosted schema
LOGO_PATH = re.compile(r'^(?![A-Za-z][A-Za-z0-9+.-]*:)(?!/)\S.*\.([Pp][Nn][Gg]|[Ss][Vv][Gg]|[Jj][Pp][Ee]?[Gg]|[Ww][Ee][Bb][Pp])$')
LOGO_URL = re.compile(r'^https://([A-Za-z0-9-]+\.)*(google\.com|gstatic\.com|googleusercontent\.com)(:[0-9]+)?([/?#].*)?$')
SEMVER = re.compile(r'^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$')
RESERVED_BRANDS = ('antigravity', 'gemini', 'claude', 'cursor')
SERVER_KEYS = {'command', 'serverUrl', 'url', 'args', 'env', 'cwd', 'headers', 'authProviderType', 'oauth',
               'disabled', 'enabledTools', 'disabledTools', 'timeoutSeconds', 'variables'}
FORBIDDEN_COPY = ('David',)   # plugin copy names Wever Labs, not an individual operator

LIVE_ENDPOINTS = {'mcp': 'https://weverlabs.com/mcp', 'mcp-free': 'https://weverlabs.com/mcp-free'}
# Tools the skill names on dedicated endpoints that this plugin does not wire.
DEDICATED_TOOLS = {'https://weverlabs.com/mcp-splits': ('wever_split-create', 'wever_split-execute',
                                                        'wever_split-status')}


class Report:
    def __init__(self):
        self.results, self.errors, self.warnings = [], [], []

    def check(self, label, ok, detail='', warn=False):
        status = 'pass' if ok else ('warning' if warn else 'error')
        self.results.append({'check': label, 'result': status, **({'detail': detail} if detail else {})})
        if not ok:
            (self.warnings if warn else self.errors).append(f'{label}: {detail}' if detail else label)
        return ok


def load_json(path, report, label):
    def pairs(items):
        keys = [key for key, _ in items]
        dupes = sorted({key for key in keys if keys.count(key) > 1})
        if dupes:
            raise ValueError(f'duplicate keys {dupes}')
        return dict(items)
    try:
        data = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)
    except (OSError, ValueError) as error:
        report.check(f'{label} parses as JSON', False, str(error))
        return None
    report.check(f'{label} parses as JSON', isinstance(data, dict), 'top level must be an object')
    return data if isinstance(data, dict) else None


def is_https(value):
    return isinstance(value, str) and value.startswith('https://') and len(value) > len('https://')


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24])
    if path.suffix.lower() == '.svg':
        box = re.search(rb'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', data)
        return (float(box.group(1)), float(box.group(2))) if box else None
    return None


def check_manifest(bundle, report):
    manifest_path = bundle / '.antigravity-plugin' / 'plugin.json'
    if not manifest_path.exists():
        manifest_path = bundle / 'plugin.json'
    if not report.check('plugin.json exists at <plugin-root>/plugin.json or .antigravity-plugin/plugin.json',
                        manifest_path.exists(), str(manifest_path)):
        return None
    manifest = load_json(manifest_path, report, 'plugin.json')
    if manifest is None:
        return None
    unknown = sorted(set(manifest) - MANIFEST_KEYS)
    report.check('plugin.json uses only schema keys (additionalProperties: false)', not unknown, f'unknown {unknown}')
    report.check('plugin.json sets no deprecated import keys', not set(manifest) & DEPRECATED_KEYS)
    report.check('$schema points at the official schema URL', manifest.get('$schema') == SCHEMA_URL,
                 'recommended for editor validation', warn=True)
    name = manifest.get('name')
    report.check('name is present (schema required)', isinstance(name, str) and bool(name))
    report.check('name matches the documented kebab-case pattern', isinstance(name, str) and bool(DOC_NAME.match(name)))
    report.check('name matches the hosted schema pattern', isinstance(name, str) and bool(SCHEMA_NAME.match(name)))
    report.check('name is the plugin folder name', name == bundle.name,
                 f'{name!r} vs folder {bundle.name!r}', warn=True)
    for key in MARKETPLACE_REQUIRED:
        report.check(f'Marketplace-required field {key} is present', key in manifest,
                     'required for Marketplace submission', warn=True)
    for key in ('displayName', 'description', 'version', 'logo', 'homepage', 'repository', 'license'):
        if key in manifest:
            report.check(f'{key} is a string', isinstance(manifest[key], str))
    display = manifest.get('displayName', '')
    for label, value in (('name', name or ''), ('displayName', display)):
        report.check(f'{label} does not lead with a reserved product brand',
                     not value.lower().startswith(RESERVED_BRANDS))
    report.check('displayName omits Plugin/MCP suffixes',
                 not re.search(r'\b(plugin|mcp)\s*$', display, re.IGNORECASE))
    description = manifest.get('description', '')
    report.check('description length is 120-160 characters (recommended)', 120 <= len(description) <= 160,
                 f'{len(description)} characters', warn=True)
    report.check('version uses MAJOR.MINOR.PATCH', bool(SEMVER.match(str(manifest.get('version', '')))),
                 'semantic versioning recommended', warn=True)
    prompts = manifest.get('suggestedPrompts')
    report.check('suggestedPrompts is a list of at most 3 non-blank strings',
                 isinstance(prompts, list) and len(prompts) <= 3
                 and all(isinstance(item, str) and item.strip() for item in prompts))
    author = manifest.get('author')
    if isinstance(author, dict):
        report.check('author object uses only name/email/url', set(author) <= {'name', 'email', 'url'})
        report.check('author.url uses https', 'url' not in author or is_https(author['url']))
        report.check('author.name is set', isinstance(author.get('name'), str) and bool(author.get('name')))
    else:
        report.check('author is a string or object', isinstance(author, str))
    for key in ('homepage', 'repository'):
        if key in manifest:
            report.check(f'{key} is a public https URL', is_https(manifest[key]))
    report.check('license is set (SPDX recommended)', bool(manifest.get('license')), warn=True)
    keywords = manifest.get('keywords', [])
    report.check('keywords are lowercase strings', isinstance(keywords, list)
                 and all(isinstance(item, str) and item == item.lower() for item in keywords))
    if 'disabled' in manifest:
        report.check('disabled is a boolean', isinstance(manifest['disabled'], bool))
    logo = manifest.get('logo')
    if logo is not None:
        bundled = isinstance(logo, str) and bool(LOGO_PATH.match(logo))
        report.check('logo is a bundled relative image path or an allowed Google-hosted URL',
                     bundled or (isinstance(logo, str) and bool(LOGO_URL.match(logo))))
        if bundled:
            target = bundle / logo
            if report.check('logo file exists inside the plugin', target.is_file() and
                            target.resolve().is_relative_to(bundle.resolve()), logo):
                size = image_size(target)
                report.check('logo is 1:1 and at least 128x128', bool(size) and size[0] == size[1] and
                             (target.suffix.lower() == '.svg' or size[0] >= 128), f'size {size}', warn=True)
    skills = manifest.get('skills')
    if skills is not None:
        paths = [skills] if isinstance(skills, str) else skills
        report.check('extra skills paths are non-blank strings', isinstance(paths, list)
                     and all(isinstance(item, str) and item.strip() for item in paths))
        for item in paths if isinstance(paths, list) else []:
            report.check(f'extra skills path {item} exists', (bundle / item).is_dir())
    return manifest


def frontmatter(text):
    """Parse the small YAML subset used by SKILL.md frontmatter (scalars and folded blocks)."""
    match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not match:
        return None
    fields, lines, index = {}, match.group(1).split('\n'), 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        key, _, value = line.partition(':')
        value = value.strip()
        if value in ('>', '>-', '|', '|-'):
            block = []
            while index < len(lines) and (lines[index].startswith(' ') or not lines[index].strip()):
                block.append(lines[index].strip())
                index += 1
            value = (' ' if value.startswith('>') else '\n').join(block).strip()
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def check_skills(bundle, manifest, report):
    roots = [bundle / 'skills']
    extra = (manifest or {}).get('skills')
    roots += [bundle / item for item in ([extra] if isinstance(extra, str) else extra or [])]
    skill_files = sorted(path for root in roots if root.is_dir() for path in root.glob('*/SKILL.md'))
    report.check('at least one skill is bundled', bool(skill_files))
    names = []
    for path in skill_files:
        label = path.relative_to(bundle).as_posix()
        fields = frontmatter(path.read_text(encoding='utf-8'))
        if not report.check(f'{label} has YAML frontmatter', fields is not None):
            continue
        name, description = fields.get('name', ''), fields.get('description', '')
        report.check(f'{label} name matches its folder', name == path.parent.name, f'{name!r}')
        report.check(f'{label} name is kebab-case, 1-64 characters',
                     bool(DOC_NAME.match(name)) and 1 <= len(name) <= 64)
        report.check(f'{label} description is 1-1024 characters', 1 <= len(description) <= 1024,
                     f'{len(description)} characters')
        names.append(name)
    return names


def check_mcp(bundle, report):
    path = bundle / 'mcp_config.json'
    if not path.exists():
        return {}
    config = load_json(path, report, 'mcp_config.json')
    if config is None:
        return {}
    report.check('mcp_config.json has only the mcpServers root key', set(config) == {'mcpServers'},
                 f'keys {sorted(config)}')
    servers = config.get('mcpServers')
    if not report.check('mcpServers is a non-empty object', isinstance(servers, dict) and bool(servers)):
        return {}
    for key, server in servers.items():
        label = f'mcpServers.{key}'
        if not report.check(f'{label} is an object', isinstance(server, dict)):
            continue
        report.check(f'{label} uses only documented properties', set(server) <= SERVER_KEYS,
                     f'unknown {sorted(set(server) - SERVER_KEYS)}')
        remote = [name for name in ('serverUrl', 'url') if name in server]
        report.check(f'{label} declares exactly one transport', (len(remote) == 1) != ('command' in server))
        for name in remote:
            report.check(f'{label}.{name} is an https Streamable HTTP endpoint', is_https(server[name]))
        report.check(f'{label} avoids unsupported httpUrl/SSE fields',
                     'httpUrl' not in server and server.get('type') not in ('sse',))
        env = server.get('env', {})
        report.check(f'{label}.env does not redefine PLUGIN_ROOT/PLUGIN_DATA',
                     isinstance(env, dict) and not {'PLUGIN_ROOT', 'PLUGIN_DATA'} & set(env))
        variables = server.get('variables')
        if variables is not None:
            report.check(f'{label}.variables is a list of named entries', isinstance(variables, list)
                         and all(isinstance(item, dict) and item.get('name') for item in variables))
    return {key: server.get('serverUrl') or server.get('url') for key, server in servers.items()
            if isinstance(server, dict)}


def check_other_components(bundle, report):
    for rule in sorted((bundle / 'rules').glob('*.md')):
        if rule.name in ('AGENTS.md', 'GEMINI.md'):
            continue
        fields = frontmatter(rule.read_text(encoding='utf-8')) or {}
        report.check(f'rules/{rule.name} declares a documented trigger',
                     fields.get('trigger') in ('always_on', 'model_decision', 'glob', 'manual'))
        if fields.get('trigger') == 'glob':
            report.check(f'rules/{rule.name} globs is a comma-separated string',
                         bool(fields.get('globs')) and not fields['globs'].startswith('['))
    hooks = bundle / 'hooks.json'
    if hooks.exists():
        data = load_json(hooks, report, 'hooks.json') or {}
        report.check('hooks.json wraps events in named hook groups',
                     all(isinstance(group, dict) for group in data.values()))
        report.check('hooks.json uses relative script paths', '${PLUGIN_ROOT}' not in hooks.read_text())
    for script in sorted((bundle / 'scripts').rglob('*')) if (bundle / 'scripts').is_dir() else []:
        if script.is_file():
            report.check(f'{script.relative_to(bundle)} is executable (0755)', script.stat().st_mode & 0o111 == 0o111)


def check_hygiene(bundle, manifest_keys, report):
    report.check('README.md is present for the Marketplace detail view',
                 (bundle / 'README.md').is_file() or (bundle / '.antigravity-plugin' / 'README.md').is_file())
    files = [path for path in bundle.rglob('*') if path.is_file() or path.is_symlink()]
    report.check('bundle contains no symlinks', not any(path.is_symlink() for path in files))
    texts = {path: path.read_text(encoding='utf-8') for path in files
             if path.suffix in ('.md', '.json', '.txt') and not path.is_symlink()}
    for term in FORBIDDEN_COPY:
        hits = sorted(path.relative_to(bundle).as_posix() for path, text in texts.items() if term in text)
        report.check(f'plugin copy does not name {term}', not hits, f'found in {hits}')
    mcp_text = texts.get(bundle / 'mcp_config.json', '')
    report.check('bundle declares no credentials, OAuth or user variables',
                 not re.search(r'"(headers|oauth|variables|authProviderType)"', mcp_text))


def parse_reference(text):
    """Return {endpoint_url: [tool names]} from references/tools.md."""
    sections, current = {}, None
    for line in text.splitlines():
        heading = re.match(r'^## .*?(https://\S+?)[)\s]', line + ' ')
        if heading:
            current = sections.setdefault(heading.group(1), [])
            continue
        row = re.match(r'^\| `([^`]+)` \|', line)
        if row and current is not None:
            current.append(row.group(1))
    return sections


def check_reference(bundle, endpoints, report):
    path = bundle / REFERENCE
    if not report.check('skill tool reference exists', path.is_file(), REFERENCE.as_posix()):
        return {}
    sections = parse_reference(path.read_text(encoding='utf-8'))
    report.check('tool reference covers every wired MCP server', set(sections) == set(endpoints.values()),
                 f'reference {sorted(sections)} vs servers {sorted(endpoints.values())}')
    for url, names in sections.items():
        report.check(f'tool reference lists unique tools for {url}', bool(names) and len(names) == len(set(names)))
    known = {name for names in sections.values() for name in names}
    known |= {name for names in DEDICATED_TOOLS.values() for name in names}
    skill = (bundle / 'skills' / 'wever-labs' / 'SKILL.md').read_text(encoding='utf-8')
    named = sorted(set(re.findall(r'`(wever_[a-z0-9_-]+)`', skill)))
    unknown = [name for name in named if name not in known]
    report.check('every wever_ tool named in SKILL.md is in the tool reference', not unknown, f'unknown {unknown}')
    return {url: len(names) for url, names in sections.items()}


def audit(bundle=BUNDLE):
    report = Report()
    manifest = check_manifest(bundle, report)
    skills = check_skills(bundle, manifest, report)
    endpoints = check_mcp(bundle, report)
    check_other_components(bundle, report)
    check_hygiene(bundle, set(manifest or {}), report)
    counts = check_reference(bundle, endpoints, report)
    name = (manifest or {}).get('name', bundle.name)
    return report, {'plugin': name, 'skills': skills,
                    'mcp_servers': {f'{name}_{key}': url for key, url in endpoints.items()},
                    'reference_tool_counts': counts}


# ---- live reference -------------------------------------------------------------------------

def price_label(description):
    text = ' '.join(description.split())
    paid = re.search(r'(\d+\.\d+) USDC per (call|mandate) on Base', text)
    if paid:
        return f'{paid.group(1)} USDC per {paid.group(2)}'
    version = re.search(r'Costs \$\d+\.\d+ \((\d+\.\d+) USDC on Base\)', text)
    if version:
        return f'{version.group(1)} USDC per version'
    if re.search(r'\bFree\b|\bis free\b|are free|No API fees|no additional buyer API fees', text):
        return 'Free'
    return 'As stated in the tool contract'


def live_tools():
    sys.path.insert(0, str(ROOT))
    from scripts.check_catalog_drift import collect_tools, request_json  # noqa: E402
    return {url: collect_tools(url, request_json) for url in
            list(LIVE_ENDPOINTS.values()) + list(DEDICATED_TOOLS)}


def render_reference(tools_by_url, today):
    main, free = LIVE_ENDPOINTS['mcp'], LIVE_ENDPOINTS['mcp-free']
    lines = ['# Wever Labs tool reference', '',
             f'Generated on {today} from the live MCP `tools/list` responses of both servers this plugin',
             'connects. Each tool description carries its full contract, inputs and price; read it before',
             'calling a tool for the first time.', '',
             f'## Main server `wever-labs_mcp` ({main}) - {len(tools_by_url[main])} tools', '',
             'Standard paid calls cost 0.10 USDC on Base mainnet through x402 after the shared allowance of',
             '10 signed-wallet free calls per rolling 30 days. The fee column repeats the access fee each',
             'tool description states. Money a tool moves, such as escrow, payouts or purchases, is separate.', '',
             '| Tool | Title | Tool fee as listed |', '| --- | --- | --- |']
    for tool in tools_by_url[main]:
        lines.append(f"| `{tool['name']}` | {tool.get('title', '')} | {price_label(tool.get('description', ''))} |")
    lines += ['', f'## Free server `wever-labs_mcp-free` ({free}) - {len(tools_by_url[free])} tools', '',
              'Every tool on this server is free and anonymous, with no wallet or account.', '',
              '| Tool | Title |', '| --- | --- |']
    for tool in tools_by_url[free]:
        lines.append(f"| `{tool['name']}` | {tool.get('title', '')} |")
    lines.append('')
    return '\n'.join(lines)


def compare_live(bundle, tools_by_url, report):
    sections = parse_reference((bundle / REFERENCE).read_text(encoding='utf-8'))
    for url in LIVE_ENDPOINTS.values():
        live = [tool['name'] for tool in tools_by_url[url]]
        ref = sections.get(url, [])
        report.check(f'tool reference matches live tools/list for {url}', live == ref,
                     f'live {len(live)}, reference {len(ref)}, added {sorted(set(live) - set(ref))}, '
                     f'removed {sorted(set(ref) - set(live))}')
    for url, expected in DEDICATED_TOOLS.items():
        live = {tool['name'] for tool in tools_by_url[url]}
        report.check(f'dedicated tools named in SKILL.md are live on {url}', set(expected) <= live,
                     f'missing {sorted(set(expected) - live)}')
    return {url: len(tools) for url, tools in tools_by_url.items()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--strict', action='store_true', help='treat warnings as errors')
    parser.add_argument('--live', action='store_true', help='compare the tool reference with live tools/list')
    parser.add_argument('--write-reference', action='store_true', help='regenerate the tool reference from live')
    parser.add_argument('--bundle', type=Path, default=BUNDLE, help='plugin root to check')
    args = parser.parse_args(argv)
    bundle = args.bundle.resolve()
    live_counts = None
    if args.write_reference or args.live:
        try:
            tools_by_url = live_tools()
        except Exception as error:  # DriftError or network failure from the shared discovery helper
            print(json.dumps({'status': 'failed', 'error': f'live discovery unavailable: {error}'}), file=sys.stderr)
            return 1
        live_counts = {url: len(tools) for url, tools in tools_by_url.items()}
        if args.write_reference:
            today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
            target = bundle / REFERENCE
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_reference(tools_by_url, today), encoding='utf-8')
    report, summary = audit(bundle)
    if args.live:
        compare_live(bundle, tools_by_url, report)
    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    print(json.dumps({'status': 'failed' if failed else 'passed', 'strict': args.strict, **summary,
                      **({'live_tool_counts': live_counts} if live_counts else {}),
                      'errors': report.errors, 'warnings': report.warnings,
                      'checks': report.results}, indent=2))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
