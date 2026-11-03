"""Offline checks for the Antigravity plugin bundle and its validator."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts import check_antigravity_plugin as plugin


def errors_for(bundle):
    report, _ = plugin.audit(bundle)
    return report.errors, report.warnings


class BundleTests(unittest.TestCase):
    def test_repository_bundle_passes_strict(self):
        report, summary = plugin.audit(plugin.BUNDLE)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])
        self.assertEqual(summary['plugin'], 'wever-labs')
        self.assertEqual(summary['skills'], ['wever-labs'])
        self.assertEqual(summary['mcp_servers'], {'wever-labs_mcp': 'https://weverlabs.com/mcp',
                                                  'wever-labs_mcp-free': 'https://weverlabs.com/mcp-free'})

    def test_manifest_matches_marketplace_copy_rules(self):
        manifest = json.loads((plugin.BUNDLE / 'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['author'], {'name': 'Wever Labs', 'url': 'https://weverlabs.com'})
        self.assertLessEqual(len(manifest['suggestedPrompts']), 3)
        self.assertTrue(120 <= len(manifest['description']) <= 160)
        self.assertEqual(manifest['logo'], 'assets/logo.svg')
        self.assertTrue((plugin.BUNDLE / manifest['logo']).is_file())

    def test_mcp_config_has_no_credentials(self):
        config = json.loads((plugin.BUNDLE / 'mcp_config.json').read_text(encoding='utf-8'))
        for server in config['mcpServers'].values():
            self.assertEqual(set(server), {'serverUrl'})


class NegativeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.bundle = Path(self.tmp.name) / 'wever-labs'
        shutil.copytree(plugin.BUNDLE, self.bundle)

    def tearDown(self):
        self.tmp.cleanup()

    def edit_json(self, name, change):
        path = self.bundle / name
        data = json.loads(path.read_text(encoding='utf-8'))
        change(data)
        path.write_text(json.dumps(data), encoding='utf-8')

    def assert_error(self, fragment):
        errors, _ = errors_for(self.bundle)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_unknown_manifest_key_fails(self):
        self.edit_json('plugin.json', lambda data: data.update(mcpServers='./mcp_config.json'))
        self.assert_error('only schema keys')

    def test_name_pattern_fails(self):
        self.edit_json('plugin.json', lambda data: data.update(name='Wever Labs'))
        self.assert_error('kebab-case pattern')

    def test_reserved_brand_prefix_fails(self):
        self.edit_json('plugin.json', lambda data: data.update(displayName='Antigravity Wever Labs'))
        self.assert_error('reserved product brand')

    def test_more_than_three_prompts_fails(self):
        self.edit_json('plugin.json', lambda data: data.update(suggestedPrompts=['a', 'b', 'c', 'd']))
        self.assert_error('suggestedPrompts')

    def test_missing_logo_file_fails(self):
        self.edit_json('plugin.json', lambda data: data.update(logo='assets/logo.png'))
        self.assert_error('logo file exists')

    def test_remote_logo_outside_google_hosts_fails(self):
        self.edit_json('plugin.json', lambda data: data.update(logo='https://weverlabs.com/icon-512.png'))
        self.assert_error('logo is a bundled relative image path')

    def test_skill_name_must_match_folder(self):
        path = self.bundle / 'skills' / 'wever-labs' / 'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8').replace('name: wever-labs', 'name: wever'), encoding='utf-8')
        self.assert_error('name matches its folder')

    def test_variables_at_config_root_fail(self):
        self.edit_json('mcp_config.json', lambda data: data.update(variables=[{'name': 'TOKEN'}]))
        self.assert_error('only the mcpServers root key')

    def test_two_transports_fail(self):
        self.edit_json('mcp_config.json', lambda data: data['mcpServers']['mcp'].update(command='node'))
        self.assert_error('exactly one transport')

    def test_plain_http_endpoint_fails(self):
        self.edit_json('mcp_config.json', lambda data: data['mcpServers']['mcp'].update(
            serverUrl='http://weverlabs.com/mcp'))
        self.assert_error('https Streamable HTTP endpoint')

    def test_unknown_skill_tool_fails(self):
        path = self.bundle / 'skills' / 'wever-labs' / 'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8') + '\nUse `wever_not-a-tool`.\n', encoding='utf-8')
        self.assert_error('every wever_ tool named in SKILL.md')

    def test_operator_name_in_copy_fails(self):
        path = self.bundle / 'README.md'
        path.write_text(path.read_text(encoding='utf-8') + '\nRun by David.\n', encoding='utf-8')
        self.assert_error('does not name David')


class ReferenceTests(unittest.TestCase):
    def tools(self, names):
        return [{'name': name, 'title': name.title(), 'description': 'Paid URL: 0.10 USDC per call on Base.'}
                for name in names]

    def test_reference_round_trip_and_drift(self):
        main, free = plugin.LIVE_ENDPOINTS['mcp'], plugin.LIVE_ENDPOINTS['mcp-free']
        live = {main: self.tools(['wever_a', 'wever_b']), free: self.tools(['wever_c'])}
        sections = plugin.parse_reference(plugin.render_reference(live, '2026-11-03'))
        self.assertEqual(sections, {main: ['wever_a', 'wever_b'], free: ['wever_c']})

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        bundle = Path(tmp.name)
        (bundle / plugin.REFERENCE).parent.mkdir(parents=True)
        (bundle / plugin.REFERENCE).write_text(plugin.render_reference(live, '2026-11-03'), encoding='utf-8')
        drifted = dict(live, **{main: self.tools(['wever_a', 'wever_b', 'wever_new'])})
        for url, names in plugin.DEDICATED_TOOLS.items():
            drifted[url] = self.tools(names)
        report = plugin.Report()
        plugin.compare_live(bundle, drifted, report)
        self.assertEqual(len(report.errors), 1)
        self.assertIn('wever_new', report.errors[0])

    def test_price_labels(self):
        cases = {
            'Paid URL: 2.00 USDC per mandate on Base; 10 free calls.': '2.00 USDC per mandate',
            'Caps 100.00 USDC per UTC day. Paid URL: 0.10 USDC per call on Base mainnet.': '0.10 USDC per call',
            'Costs $2.00 (2.00 USDC on Base). POST /api/mandate-issue.': '2.00 USDC per version',
            'Read status. Free. POST /api/mandate-status.': 'Free',
            'Record a simulated shipment.': 'As stated in the tool contract',
        }
        for description, expected in cases.items():
            with self.subTest(description=description):
                self.assertEqual(plugin.price_label(description), expected)

    def test_frontmatter_folded_block(self):
        fields = plugin.frontmatter('---\nname: demo\ndescription: >-\n  One line\n  two line.\n---\nBody\n')
        self.assertEqual(fields, {'name': 'demo', 'description': 'One line two line.'})


if __name__ == '__main__':
    unittest.main()
