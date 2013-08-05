import os
import logging
import argparse

from divvy import root, sync, fetch


def main():
    parser = argparse.ArgumentParser(description='Divvy CLI')
    parser.add_argument('command', choices=['fetch', 'sync'])
    parser.add_argument('--datadir', default=os.path.join(root, 'data'))
    parser.add_argument('--token', default=os.environ.get('GITHUB_TOKEN', ''))
    parser.add_argument('--branch', default=os.environ.get('GIT_BRANCH', 'master'))
    parser.add_argument('-v', '--verbose', action='store_true')
    opts = parser.parse_args()

    level = logging.DEBUG if opts.verbose else logging.INFO
    logging.basicConfig(level=level)

    repo = dict(owner='chbrown', repo='divvy-history', branch=opts.branch)

    headers = dict(Authorization='token ' + opts.token)

    if opts.command == 'fetch':
        fetch.fetch(opts.datadir)
    elif opts.command == 'sync':
        sync.sync(opts.datadir, repo, headers)
    else:
        print 'Invalid command'
