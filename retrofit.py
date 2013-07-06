#!/usr/bin/env python
import os
import json
from datetime import datetime
from jsonpatch import JsonPatch
import pytz

CDT = pytz.timezone('America/Chicago')

# old-style files:
# stations-epoch.json -- some beginning point to enact patches on top of
# patches.json -- list of json-patches changes to get from epoch to current
# stations-current.json -- the current stations

# this file converts from old-format stations-epoch.json + patches.json to
# new-style dates/YYYY-MM-DD.{json,patches} format


def update(date, current_stations):
    print 'Updating to %s' % date
    date_stations = os.path.join('dates', date + '.json')
    date_patches = os.path.join('dates', date + '.patches')

    if not os.path.exists(date_stations):
        with open(date_stations, 'w') as fp:
            json.dump(current_stations, fp)
        print 'Created file %s with %d-long stationBeanList' % (
            date_stations, len(current_stations['stationBeanList']))
    else:
        # load beginning-of-day patches
        old_stations = json.load(open(date_stations))
        with open(date_patches, 'a+') as fp:
            # apply patches, one by one
            for line in open(date_patches, 'r'):
                patch = JsonPatch.from_string(line)
                patch.apply(old_stations, in_place=True)

            # get the bleeding edge (changes in the last minute)
            json_patch = JsonPatch.from_diff(old_stations, current_stations)

            print 'Writing %d patches to %s' % (len(json_patch.patch), date_patches)
            if len(json_patch.patch) > 0:
                json.dump(json_patch.patch, fp)
                fp.write('\n')


# in case we are *really* retrofitting:
if not os.path.exists('dates'):
    os.mkdir('dates')

# load the very beginning stations (we don't care about stations-current.json)
current_stations = json.load(open('stations-epoch.json'))

# apply the patches incrementally
for line_i, patch_string in enumerate(open('patches.json', 'r')):
    naive_date = datetime.strptime(current_stations['executionTime'], '%Y-%m-%d %I:%M:%S %p')
    utc_date = CDT.localize(naive_date).astimezone(pytz.utc)
    print 'Line #%4d, UTC: %s' % (line_i, utc_date.isoformat())
    date = utc_date.strftime('%Y-%m-%d')

    update(date, current_stations)

    # finally, apply patch
    patch = JsonPatch.from_string(patch_string)
    patch.apply(current_stations, in_place=True)

update(date, current_stations)

print 'Completely retrofitted. Removing retro files:'
for filename in ['stations-current.json', 'stations-epoch.json', 'patches.json']:
    print 'rm', filename
    os.remove(filename)
