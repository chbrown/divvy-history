import os

bind = '0.0.0.0:5080'
accesslog = '-'
errorlog = '-'
loglevel = 'debug'  # e.g.: debug info warning error critical

datadir = 'data'
github_token = os.environ.get('GITHUB_TOKEN', '')
git_branch = os.environ.get('GIT_BRANCH', 'master')
repo = dict(owner='chbrown', repo='divvy-history', branch=git_branch)
