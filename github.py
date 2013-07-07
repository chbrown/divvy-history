#!/usr/bin/env python
import os
import requests
import pprint

repo = dict(owner='chbrown', repo='divvy-history', branch='dates')


def api(url, method='GET', **params):
    headers = dict(Authorization='token ' + os.environ['GITHUB_TOKEN'])
    return requests.request(method, 'https://api.github.com' + url, headers=headers, params=params)


def hashes():
    import glob
    import hashlib
    for file_path in glob.glob('data/*'):
        file_size = os.path.getsize(file_path)
        with open(file_path) as fp:
            file_data = fp.read()

        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=file_path, **repo)
        response = api(url, 'GET', ref=repo['branch'])
        result = response.json()
        print 'Getting file contents... status:', response.status_code
        # pprint.pprint(result)

        shahash = hashlib.sha1('blob %d\0' % file_size)
        shahash.update(file_data)
        local_sha = shahash.hexdigest()
        remote_sha = result.get('sha')
        print file_path, local_sha, remote_sha


def main():
    import argparse
    parser = argparse.ArgumentParser(description='GitHub API explorer')
    parser.add_argument('action')
    # parser.add_argument('local', nargs='?')
    opts = parser.parse_args()

    if opts.action == 'hashes':
        hashes()

if __name__ == '__main__':
    main()
