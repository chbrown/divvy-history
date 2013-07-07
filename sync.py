import os
import glob
import requests
# import argparse
import base64
import datetime
import pprint
import hashlib

repo = dict(owner='chbrown', repo='divvy-history', branch='dates')

# github_name = os.environ['GITHUB_NAME']
# github_email = os.environ['GITHUB_EMAIL']
# 'author.name': github_name,
# 'author.email': github_email

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='')
#     parser.add_argument('remote')
#     parser.add_argument('local', nargs='?')
#     opts = parser.parse_args()

#     remote_flat = opts.remote.replace(':/', '/').replace(':', '/home/')
#     local = opts.local or '/Volumes/%s' % remote_flat
#     mkdir_p(local)


def api(url, method='GET', **params):
    headers = dict(Authorization='token ' + os.environ['GITHUB_TOKEN'])
    return requests.request(method, 'https://api.github.com' + url, headers=headers, params=params)


def put_file(data, path, sha=None):
    url = '/repos/{owner}/{repo}/contents/{path}'.format(path=path, **repo)

    # upload the file
    data_base64 = base64.b64encode(data)

    # PUT /repos/:owner/:repo/contents/:path
    message = 'utc=' + datetime.datetime.utcnow().isoformat()
    params = dict(message=message, content=data_base64, branch=repo['branch'])
    if sha:
        # if the file already exists, we must update it by also providing the previous sha
        params['sha'] = sha

    r = api(url, 'PUT', **params)
    pprint.pprint(r.headers)
    pprint.pprint(r.text)


def sync():
    # repo = gh.get_repo('chbrown/divvy-history')
    for file_path in glob.glob('*/**.json'):
        file_size = os.path.getsize(file_path)
        with open(file_path) as fp:
            file_data = fp.read()

        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=file_path, **repo)
        res = api(url, 'GET', ref=repo['branch'])
        print 'GET status: ' + res.status_code

        local_sha = hashlib.sha1('blob ' + file_size + '\0' + file_data)
        remote_sha = res.get('sha')

        # upload if 1) the file doesn't already exist, or 2) the local sha is different
        print '{file}: local={local_sha} remote={remote_sha}'.format(
            file=file_path, local_sha=local_sha, remote_sha=remote_sha)
        if remote_sha != local_sha:
            # r.status_code != 404
            put_file(file_data, file_path, remote_sha)

        # if r.headers.status.

        # git commit -a -m "epoch=`date +%s`"


def api_print(url, method='GET', **params):
    response = api(url, method, **params)

    pprint(response.json())
    return

if __name__ == '__main__':
    sync()

# api_print('/user')
# api_print('/user/emails')
# api_print('/users/dssg')
# api_print('/users/chbrown/events/orgs/dssg')
# api_print('/repos/chbrown/sv/issues', state='closed')
# api_print('/repos/dssg/dssg-twitter-disaster/issues', state='open')
# api_print('/user/issues')
# /orgs/dssg/members

