#!/usr/bin/env python3
"""Check metadata revision consistency and the independently observed MCP runtime."""
import argparse
import json
from pathlib import Path
import re
import sys

try:
    from . import check_catalog_drift as drift
except ImportError:
    import check_catalog_drift as drift

ROOT = Path(__file__).resolve().parents[1]
FILES = ('server.json', 'server.dns-auth.example.json', 'lhm.plugin.json', 'package.json')
PUBLISHER = 'io.modelcontextprotocol.registry/publisher-provided'


def read_manifests(published=False):
    return {name: drift.decode_json(
        drift.fetch_text(drift.PUBLIC_REGISTRY + name) if published else (ROOT / name).read_text(),
        name) for name in FILES}


def validate_metadata_versions(manifests, server_info):
    try:
        version = manifests['server.json']['version']
        drift.require(isinstance(version, str) and re.fullmatch(r'\d+\.\d+\.\d+(?:-registry\.\d+)?', version),
                      'Registry metadata version must be an explicit semantic revision')
        for name in FILES:
            drift.require(manifests[name]['version'] == version, name + ': registry metadata version differs')
        hosted = manifests['server.json']['_meta'][PUBLISHER]['hostedServerVersion']
        drift.require(isinstance(hosted, str) and re.fullmatch(r'\d+\.\d+\.\d+', hosted),
                      'Hosted server version must be explicit')
        drift.require(manifests['server.dns-auth.example.json']['_meta'][PUBLISHER]['hostedServerVersion'] == hosted,
                      'DNS descriptor hosted server version differs')
        drift.require(server_info['name'] == manifests['server.json']['name'], 'Live MCP server identity differs')
        drift.require(server_info['version'] == hosted, 'Live MCP hosted server version differs')
        return {'metadata_version': version, 'hosted_server_version': hosted}
    except (KeyError, TypeError) as error:
        raise drift.DriftError('Missing or malformed registry version metadata: ' + str(error)) from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--published', action='store_true')
    args = parser.parse_args(argv)
    try:
        response = drift.request_json(drift.MAIN, {
            'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
            'params': {'protocolVersion': '2025-03-26', 'capabilities': {},
                       'clientInfo': {'name': 'wever-registry-version-check', 'version': '1.0.0'}}})
        drift.require(response.get('jsonrpc') == '2.0' and response.get('id') == 1
                      and 'error' not in response, 'Invalid MCP initialize response')
        info = response['result']['serverInfo']
        local = validate_metadata_versions(read_manifests(), info)
        if args.published:
            published = validate_metadata_versions(read_manifests(True), info)
            drift.require(published == local, 'Published metadata and hosted versions differ from local')
        print(json.dumps({'status': 'passed', **local, 'published_checked': args.published}, indent=2))
        return 0
    except (drift.DriftError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
