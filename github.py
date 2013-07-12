#!/usr/bin/env python
import os
import json
import requests

from settings import repo, datadir

headers = dict(Authorization='token ' + os.environ['GITHUB_TOKEN'])
root = 'https://api.github.com'


def _jsondefault(obj):
    if isinstance(obj, requests.structures.CaseInsensitiveDict):
        return dict(obj.items())
    return obj


def inspect(obj, indent=2, prefix='  '):
    string = json.dumps(obj, indent=indent, default=_jsondefault, sort_keys=True)
    return string.replace('\n', '\n' + prefix)


def hashes():
    import glob
    import hashlib
    for file_path in glob.glob('data/*'):
        file_size = os.path.getsize(file_path)
        with open(file_path) as fp:
            file_data = fp.read()

        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=file_path, **repo)
        params = dict(ref=repo['branch'])
        response = requests.get(root + url, headers=headers, params=params)
        result = response.json()
        print 'Getting file contents... status:', response.status_code

        shahash = hashlib.sha1('blob %d\0' % file_size)
        shahash.update(file_data)
        local_sha = shahash.hexdigest()
        remote_sha = result.get('sha')
        print file_path, local_sha, remote_sha


def listfiles():
    # import pprint
    url = '/repos/{owner}/{repo}/contents/{path}'.format(path=datadir, **repo)
    params = dict(ref=repo['branch'])
    response = requests.get(root + url, headers=headers, params=params)
    result = response.json()
    print 'Getting directory:', datadir
    print 'Response status code:', response.status_code
    print inspect(result)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='GitHub API explorer')
    parser.add_argument('action')
    # parser.add_argument('local', nargs='?')
    opts = parser.parse_args()

    if opts.action == 'hashes':
        hashes()
    elif opts.action == 'listfiles':
        listfiles()
    else:
        print 'Action not implemented:', opts.action

if __name__ == '__main__':
    main()
