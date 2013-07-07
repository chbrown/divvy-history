#!/usr/bin/env python
import os
import glob
import base64
import datetime
import hashlib
from logger import logger
import github

repo = dict(owner='chbrown', repo='divvy-history', branch='dates')

# github_name = os.environ['GITHUB_NAME']
# github_email = os.environ['GITHUB_EMAIL']
# 'author.name': github_name,
# 'author.email': github_email


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

    response = github.api(url, 'PUT', **params)
    logger.debug('PUT response headers: %s', response.headers)
    logger.debug('PUT response body: %s', response.text)


def sync():
    now = datetime.datetime.utcnow()
    logger.debug('Syncing started: %s', now.isoformat())
    for file_path in glob.glob('data/*'):
        file_size = os.path.getsize(file_path)
        with open(file_path) as fp:
            file_data = fp.read()

        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=file_path, **repo)
        response = github.api(url, 'GET', ref=repo['branch'])
        result = response.json()
        logger.debug('Getting file contents... status: %s', response.status_code)

        shahash = hashlib.sha1('blob %d\0' % file_size)
        shahash.update(file_data)
        local_sha = shahash.hexdigest()
        remote_sha = result.get('sha')

        # upload if 1) the file doesn't already exist, or 2) the local sha is different
        logger.debug('{file_path}: local={local_sha} remote={remote_sha}'.format(
            file_path=file_path, local_sha=local_sha, remote_sha=remote_sha))
        raise Exception('Stopping')
        if remote_sha != local_sha:
            # r.status_code != 404
            put_file(file_data, file_path, remote_sha)

        # if r.headers.status.
        # git commit -a -m "epoch=`date +%s`"

if __name__ == '__main__':
    sync()
