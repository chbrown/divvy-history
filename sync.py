#!/usr/bin/env python
import os
import glob
import json
import datetime
import base64
import hashlib
import requests

import github
from logger import logger
from settings import repo


def put_file(file_data, file_path, sha=None):
    url = '/repos/{owner}/{repo}/contents/{path}'.format(path=file_path, **repo)

    # upload the file
    file_data_base64 = base64.b64encode(file_data)

    # PUT /repos/:owner/:repo/contents/:path
    now = datetime.datetime.utcnow()
    message = 'utc={now} file={file_path}'.format(now=now.isoformat(), file_path=file_path)
    params = dict(message=message, content=file_data_base64, branch=repo['branch'])
    if sha:
        # if the file already exists, we must update it by also providing the previous sha
        params['sha'] = sha

    headers = dict(github.headers.items() + [('Content-type', 'application/json')])
    data = json.dumps(params)
    response = requests.put(github.root + url, headers=headers, data=data)
    result = response.json()
    logger.debug('PUT %s: %d', url, response.status_code)
    logger.debug('req headers: %s', github.inspect(response.request.headers))
    # logger.debug('req body: %s', response.request.body)
    logger.debug('res headers: %s', github.inspect(response.headers))
    logger.debug('res body: %s', github.inspect(result))


def sync():
    now = datetime.datetime.utcnow()
    logger.debug('Syncing started: %s', now.isoformat())
    for file_path in glob.glob('data/*'):
        file_size = os.path.getsize(file_path)
        with open(file_path) as fp:
            file_data = fp.read()

        url = '/repos/{owner}/{repo}/contents/{path}'.format(path=file_path, **repo)
        params = dict(ref=repo['branch'])
        response = requests.get(github.root + url, headers=github.headers, params=params)
        result = response.json()
        logger.debug('GET %s: %d', url, response.status_code)

        shahash = hashlib.sha1('blob %d\0' % file_size)
        shahash.update(file_data)
        local_sha = shahash.hexdigest()
        remote_sha = result.get('sha')

        # upload if 1) the file doesn't already exist, or 2) the local sha is different
        logger.debug('%s: local=%s remote=%s (ref=%s)', file_path, local_sha, remote_sha, repo['branch'])
        if remote_sha != local_sha:
            # r.status_code != 404
            put_file(file_data, file_path, remote_sha)

        # if r.headers.status.
        # git commit -a -m "epoch=`date +%s`"

if __name__ == '__main__':
    sync()
