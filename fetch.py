#!/usr/bin/env python
import os
import json
import urllib
import datetime
from jsonpatch import JsonPatch
from logger import logger


def fetch():
    now = datetime.datetime.utcnow()
    logger.debug('Fetching started: %s', now.isoformat())

    url = 'http://divvybikes.com/stations/json'

    # set date (e.g., '2013-07-06')
    date = now.strftime('%Y-%m-%d')
    date_stations = os.path.join('data', date + '.json')
    date_patches = os.path.join('data', date + '.patches')

    # basic process:
    # 1. open the local stations/json file
    # 2. apply all the patches
    # 3. get the most recent stations/json file from the web
    # 4. write the patch for the current state

    if not os.path.exists(date_stations):
        filepath, http_message = urllib.urlretrieve(url)
        os.rename(filepath, date_stations)
        logger.debug('Created file: %s', date_stations)
    else:
        # load beginning-of-day patches
        old_stations = json.load(open(date_stations))
        logger.debug('Opening file %s in a+ mode', date_patches)
        with open(date_patches, 'a+') as fp:
            # with the a+ we have to seek to the beginning,
            # but any writes will automatically be written at the end
            fp.seek(0)
            line_i = 0
            # apply patches, one by one
            for line_i, line in enumerate(fp):
                patch = JsonPatch.from_string(line)
                patch.apply(old_stations, in_place=True)
            logger.debug('Read %d patches from %s', line_i, date_patches)

            # get the bleeding edge (changes in the last minute)
            filepath, http_message = urllib.urlretrieve(url)
            current_stations = json.load(open(filepath))
            json_patch = JsonPatch.from_diff(old_stations, current_stations)

            if len(json_patch.patch) > 0:
                json.dump(json_patch.patch, fp)
                fp.write('\n')
            logger.debug('Added patch with %d changes to %s', len(json_patch.patch), date_patches)

if __name__ == '__main__':
    fetch()
