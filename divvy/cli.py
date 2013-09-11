import os
import logging
import argparse

from divvy import root, sync, fetch, scheduling


def main():
    parser = argparse.ArgumentParser(description='Divvy CLI',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('command', choices=['fetch', 'sync', 'push', 'poll'])
    parser.add_argument('--datadir', default=os.path.join(root, 'data'),
        help='Directory to save datestamped files')
    parser.add_argument('--token', default=os.environ.get('GITHUB_TOKEN', ''),
        help='Github API token')
    parser.add_argument('--branch', default=os.environ.get('GIT_BRANCH', 'master'),
        help='Git repository branch to use')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='Print extra output')
    opts = parser.parse_args()

    level = logging.DEBUG if opts.verbose else logging.INFO
    logging.basicConfig(level=level)

    repo = dict(owner='chbrown', repo='divvy-history', branch=opts.branch)

    headers = dict(Authorization='token ' + opts.token)

    if opts.command == 'fetch':
        fetch.fetch(opts.datadir)
    elif opts.command == 'sync':
        sync.sync(opts.datadir, repo, headers)
    elif opts.command == 'push':
        sync.git_commit_push(opts.datadir)
    elif opts.command == 'poll':
        scheduling.poll(opts.datadir)
    else:
        print 'Invalid command'
