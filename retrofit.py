#!/usr/bin/env python
import sys
import os
import json
from datetime import datetime
from jsonpatch import JsonPatch
import pytz

# relative imports
if '.' not in sys.path:
    sys.path.insert(0, '.')
from patching import persist_new_state
from logger import logger
from settings import datadir

CDT = pytz.timezone('America/Chicago')

# this file converts from old-format stations-epoch.json + patches.json to

# before (old-style):
#   stations-epoch.json -- some beginning point to enact patches on top of
#   patches.json -- list of json-patches changes to get from epoch to current
#   stations-current.json -- the current stations

# after (new-style):
#   data/YYYY-MM-DD.{json,patches} -- for each day that's been covered, about 1440 patches per day

if not os.path.exists(datadir):
    os.mkdir(datadir)
    logger.warn('Created directory: %s', datadir)
else:
    logger.info('Directory already exists: %s', datadir)

# load the very beginning stations (we don't care about stations-current.json)
current_state = json.load(open('stations-epoch.json'))
CACHE = dict()

# do a simple line count on the old-style patches file
for total_patches, _ in enumerate(open('patches.json')):
    pass

logger.info('Retrofitting %d patchsets', total_patches)


def flush(date_string):
    epoch_path = os.path.join(datadir, date_string + '.json')
    patches_path = os.path.join(datadir, date_string + '.patches')
    persist_new_state(epoch_path, patches_path, current_state, logger=logger, cache=CACHE)

# apply the patches incrementally
for patch_i, patch_string in enumerate(open('patches.json')):
    # this datetime conversion determines how we split up files (by UTC date, but not time)
    naive_date = datetime.strptime(current_state['executionTime'], '%Y-%m-%d %I:%M:%S %p')
    utc_date = CDT.localize(naive_date).astimezone(pytz.utc)

    logger.warn('Line #%5d/%5d, UTC: %s', patch_i, total_patches, utc_date.isoformat())

    date_string = utc_date.strftime('%Y-%m-%d')
    flush(date_string)

    patch = JsonPatch.from_string(patch_string)
    patch.apply(current_state, in_place=True)
else:
    flush(date_string)

logger.error('Completely retrofitted. Removing retro files.')
for filename in ['stations-current.json', 'stations-epoch.json', 'patches.json']:
    logger.error('rm %s', filename)
    os.remove(filename)
