import os
import sys
import time
import datetime
from apscheduler.scheduler import Scheduler
from bottle import Bottle, mako_view

# sys.path is a global for this python thread, so this enables local imports throughout the app
sys.path.insert(0, '.')
from fetch import fetch
from settings import datadir
from sync import sync
from logger import logger

schedule = Scheduler()
schedule.start()
schedule.add_interval_job(fetch, minutes=1)
schedule.add_interval_job(sync, hours=6)
# schedule.add_interval_job(sync, minutes=5)

now = datetime.datetime.utcnow()
logger.debug('Scheduler initialized. UTC=%s', now.isoformat())

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
    filenames = sorted(os.listdir(datadir))
    filepaths = [os.path.join(datadir, filename) for filename in filenames]
    files = [dict(name=filepath, lines=linecount(filepath)) for filepath in sorted(filepaths)]
    return dict(files=files)


@application.route('/fetch')
def get_fetch():
    started = time.time()
    fetch()
    ended = time.time()
    return 'Fetch done. Took %0.2f seconds.' % (ended - started)


@application.route('/sync')
def get_sync():
    started = time.time()
    sync()
    ended = time.time()
    return 'Sync done. Took %0.2f seconds.' % (ended - started)
