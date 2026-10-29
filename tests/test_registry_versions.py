"""Registry-only revisions must retain an independently verified runtime version."""
import contextlib
import copy
import io
import json
import unittest
from unittest.mock import patch

from scripts import check_registry_versions as versions


def fixture():
    manifest = {'version': '0.8.1-registry.1', 'name': 'io.github.CodeWever/wever-labs-products',
                '_meta': {versions.PUBLISHER: {'hostedServerVersion': '0.8.0'}}}
    return {name: copy.deepcopy(manifest) for name in versions.FILES}


class VersionTests(unittest.TestCase):
    def setUp(self):
        self.manifests = fixture()
        self.info = {'name': 'io.github.CodeWever/wever-labs-products', 'version': '0.8.0'}

    def test_metadata_revision_and_runtime_are_verified_separately(self):
        self.assertEqual(versions.validate_metadata_versions(self.manifests, self.info),
                         {'metadata_version': '0.8.1-registry.1', 'hosted_server_version': '0.8.0'})

    def test_each_metadata_version_must_match(self):
        for name in versions.FILES:
            with self.subTest(name=name):
                changed = copy.deepcopy(self.manifests)
                changed[name]['version'] = '0.8.2-registry.1'
                with self.assertRaises(versions.drift.DriftError):
                    versions.validate_metadata_versions(changed, self.info)

    def test_missing_hosted_version_fails_in_either_descriptor(self):
        for name in ('server.json', 'server.dns-auth.example.json'):
            with self.subTest(name=name):
                changed = copy.deepcopy(self.manifests)
                del changed[name]['_meta'][versions.PUBLISHER]['hostedServerVersion']
                with self.assertRaises(versions.drift.DriftError):
                    versions.validate_metadata_versions(changed, self.info)

    def test_wrong_hosted_version_fails_against_live_runtime(self):
        for name in ('server.json', 'server.dns-auth.example.json'):
            self.manifests[name]['_meta'][versions.PUBLISHER]['hostedServerVersion'] = '0.8.1'
        with self.assertRaisesRegex(versions.drift.DriftError, 'Live MCP hosted'):
            versions.validate_metadata_versions(self.manifests, self.info)

    def test_mismatched_hosted_versions_fail(self):
        self.manifests['server.dns-auth.example.json']['_meta'][versions.PUBLISHER]['hostedServerVersion'] = '0.8.1'
        with self.assertRaisesRegex(versions.drift.DriftError, 'DNS descriptor'):
            versions.validate_metadata_versions(self.manifests, self.info)

    def test_wrong_runtime_identity_fails(self):
        self.info['name'] = 'io.github.other/server'
        with self.assertRaisesRegex(versions.drift.DriftError, 'identity'):
            versions.validate_metadata_versions(self.manifests, self.info)

    def test_published_versions_are_independently_checked(self):
        response = {'jsonrpc': '2.0', 'id': 1, 'result': {'serverInfo': self.info}}
        stale = fixture()
        for manifest in stale.values():
            manifest['version'] = '0.8.2-registry.1'
        with patch.object(versions.drift, 'request_json', return_value=response), \
             patch.object(versions, 'read_manifests', side_effect=[self.manifests, stale]), \
             contextlib.redirect_stderr(io.StringIO()) as output:
            self.assertEqual(versions.main(['--published']), 1)
            self.assertIn('Published metadata', json.loads(output.getvalue())['error'])

    def test_cli_success_and_rpc_error(self):
        response = {'jsonrpc': '2.0', 'id': 1, 'result': {'serverInfo': self.info}}
        with patch.object(versions.drift, 'request_json', return_value=response), \
             patch.object(versions, 'read_manifests', return_value=self.manifests), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(versions.main([]), 0)
            self.assertEqual(json.loads(output.getvalue())['hosted_server_version'], '0.8.0')
        with patch.object(versions.drift, 'request_json', return_value={'jsonrpc': '2.0', 'id': 1, 'error': {}}), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(versions.main([]), 1)


if __name__ == '__main__':
    unittest.main()
