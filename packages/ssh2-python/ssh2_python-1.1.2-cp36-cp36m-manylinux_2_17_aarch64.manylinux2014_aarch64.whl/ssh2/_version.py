
import json

version_json = '''
{"date": "2025-01-23T02:17:37.328454", "dirty": false, "error": null, "full-revisionid": "a61495cf442d08362d0ca3f213eeb8eb9e074cac", "version": "1.1.2"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

