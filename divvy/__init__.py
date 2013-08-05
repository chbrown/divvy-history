import os
import logging

logging.basicConfig(level=logging.INFO)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
datadir = os.path.join(root, 'data')

github_token = os.environ.get('GITHUB_TOKEN', '')
git_branch = os.environ.get('GIT_BRANCH', 'master')
repo = dict(owner='chbrown', repo='divvy-history', branch=git_branch)
