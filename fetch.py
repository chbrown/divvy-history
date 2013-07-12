#!/usr/bin/env python
import os
import sys
import json
import time
import urllib
import datetime

# relative imports
if '.' not in sys.path:
    sys.path.insert(0, '.')
from patching import persist_new_state
from logger import logger
from settings import datadir


def fetch():
    utc_date = datetime.datetime.utcnow()
    logger.debug('Fetching started: %s', utc_date.isoformat())

    url = 'http://divvybikes.com/stations/json'

    # set date (e.g., '2013-07-06')
    date_string = utc_date.strftime('%Y-%m-%d')

    epoch_path = os.path.join(datadir, date_string + '.json')
    patches_path = os.path.join(datadir, date_string + '.patches')

    # basic process:
    # 1. open the local stations/json file
    # 2. apply all the patches
    # 3. get the most recent stations/json file from the web
    # 4. write the patch for the current state

    if not os.path.exists(epoch_path):
        filepath, http_message = urllib.urlretrieve(url)
        os.rename(filepath, epoch_path)
        logger.debug('Downloaded original directly to file: %s', epoch_path)
    else:
        # get the bleeding edge (changes in the last minute)
        filepath, http_message = urllib.urlretrieve(url)
        current_state = json.load(open(filepath))

        # load beginning-of-day patches
        started = time.time()
        logger.info('Persisting new state to epoch-patches pair: %s, %s', epoch_path, patches_path)
        persist_new_state(epoch_path, patches_path, current_state, logger=logger)
        ended = time.time()
        logger.info('Finished persisting new state in %0.2f seconds.', ended - started)

if __name__ == '__main__':
    fetch()
