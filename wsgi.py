import os
import glob
import sys
import json
import datetime
from apscheduler.scheduler import Scheduler
from bottle import Bottle, mako_view

# sys.path is a global for this python thread, so this enables local imports throughout the app
sys.path.insert(0, '.')
from fetch import fetch
from sync import sync
from logger import logger

schedule = Scheduler()
schedule.start()
schedule.add_interval_job(fetch, minutes=1)
# schedule.add_interval_job(sync, hours=6)
schedule.add_interval_job(sync, minutes=5)

now = datetime.datetime.utcnow()
logger.debug('Scheduler initialized. %s', now.isoformat())

application = Bottle()


def linecount(filepath):
    lines = -1
    with open(filepath, 'rb') as fp:
        for lines, _ in enumerate(fp):
            pass
    return lines


@application.route('/')
@mako_view('index.mako')
def index():
    filenames = glob.glob('data/*')
    files = [dict(name=filename, lines=linecount(filename)) for filename in sorted(filenames)]
    return dict(files=files)


@application.route('/pwd')
def pwd():
    return os.getcwd()


@application.route('/login')
def login():
    return os.getlogin()


@application.route('/env')
@mako_view('code.mako')
def env():
    body = json.dumps(dict(os.environ.items()), indent=2)
    return dict(body=body)


# @application.route('/config')
# @mako_view('code.mako')
# def config():
#     body = open('gunicorn.config').read()
#     return dict(body=body)


@application.route('/dot')
@mako_view('code.mako')
def dot():
    files = os.listdir('.')
    body = json.dumps(files, indent=2)
    return dict(body=body)
