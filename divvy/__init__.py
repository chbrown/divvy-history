import os.path
import json
import requests

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _jsondefault(obj):
    if isinstance(obj, requests.structures.CaseInsensitiveDict):
        return dict(obj.items())
    return obj


def inspect(obj, indent=2, prefix='  '):
    string = json.dumps(obj, indent=indent, default=_jsondefault, sort_keys=True)
    return string.replace('\n', '\n' + prefix)
