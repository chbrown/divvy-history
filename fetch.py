#!/usr/bin/env python
import os
import json
import urllib
from datetime import datetime
from jsonpatch import JsonPatch


def fetch():
    print 'Fetching', datetime.utcnow().isoformat()

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

if __name__ == '__main__':
    fetch()
