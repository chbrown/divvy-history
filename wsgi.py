import os
import json
import urllib
from datetime import datetime
from jsonpatch import JsonPatch
from apscheduler.scheduler import Scheduler
from bottle import Bottle, mako_view
application = Bottle()


def linecount(filename):
    lines = -1
    with open(filename, 'rb') as fp:
        for lines, _ in enumerate(fp):
            pass
    return lines


@application.route('/')
@mako_view('index.mako')
def index():
    filenames = ['dates/' + filename for filename in os.listdir('dates')]
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


@application.route('/config')
@mako_view('code.mako')
def config():
    body = open('gunicorn.config').read()
    return dict(body=body)


@application.route('/dot')
@mako_view('code.mako')
def dot():
    files = os.listdir('.')
    body = json.dumps(files, indent=2)
    return dict(body=body)


def fetch():
    print "Fetching", datetime.utcnow().isoformat()

    url = 'http://divvybikes.com/stations/json'

    # set date (e.g., '2013-07-06')
    date = datetime.utcnow().strftime('%Y-%m-%d')
    date_stations = os.path.join('dates', date + '.json')
    date_patches = os.path.join('dates', date + '.patches')

    # basic process:
    # 1. open the local stations/json file
    # 2. apply all the patches
    # 3. get the most recent stations/json file from the web
    # 4. write the patch for the current state

    if not os.path.exists(date_stations):
        filepath, http_message = urllib.urlretrieve(url)
        os.rename(filepath, date_stations)
    else:
        # load beginning-of-day patches
        old_stations = json.load(open(date_stations))
        with open(date_patches, 'a+') as fp:
            # apply patches, one by one
            for line in open(date_patches, 'r'):
                patch = JsonPatch.from_string(line)
                patch.apply(old_stations, in_place=True)

            # get the bleeding edge (changes in the last minute)
            filepath, http_message = urllib.urlretrieve(url)
            current_stations = json.load(open(filepath))
            json_patch = JsonPatch.from_diff(old_stations, current_stations)

            if len(json_patch.patch) > 0:
                json.dump(json_patch.patch, fp)
                fp.write('\n')


schedule = Scheduler()
schedule.start()
schedule.add_interval_job(fetch, minutes=1)
