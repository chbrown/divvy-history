'''This script should be called at least once a minute'''
import os
import json
import time
import urllib
import shutil
import logging
import datetime
from jsonpatch import JsonPatch

logger = logging.getLogger(__name__)


def merge_epoch_and_patches(epoch_path, patches_path):
    # read the 0-day (original) file
    with open(epoch_path) as epoch_fp:
        obj = json.load(epoch_fp)

    # apply patches, one by one
    patches_applied = 0
    if os.path.exists(patches_path):
        with open(patches_path) as patches_fp:
            for patch_line in patches_fp:
                patch = JsonPatch.from_string(patch_line)
                patch.apply(obj, in_place=True)
                patches_applied += 1

    logger.info('Read %d patchsets from %s and applied them to %s', patches_applied, patches_path, epoch_path)

    return obj


def persist_new_state(epoch_path, patches_path, new_state, persisted_state_cache=None):
    '''
    Read in the original file, apply patches, and add patch for diff between
    filesystem state and the provided new_state argument.
    '''
    if not os.path.exists(epoch_path):
        with open(epoch_path, 'w') as epoch_fp:
            json.dump(new_state, epoch_fp)
        logger.info('Created file: %s', epoch_path)
    else:
        # load 0-day json and merge with patches.

        cache_key = epoch_path + ':' + patches_path
        persisted_state = persisted_state_cache.get(cache_key) if persisted_state_cache is not None else None
        if not persisted_state:
            logger.debug('Cache miss (%s), loading from epoch-patches pair: %s, %s', cache_key, epoch_path, patches_path)
            persisted_state = merge_epoch_and_patches(epoch_path, patches_path)
        else:
            logger.info('Previous state retrieved from cache: %s', cache_key)

        diff = JsonPatch.from_diff(persisted_state, new_state)
        if len(diff.patch) > 0:
            with open(patches_path, 'a') as patches_fp:
                logger.warn('Writing %d patches to %s', len(diff.patch), patches_path)
                json.dump(diff.patch, patches_fp)
                patches_fp.write(os.linesep)
        else:
            logger.info('No patches to write to %s', patches_path)

        if persisted_state_cache is not None:
            logger.debug('Adding state to persisted cache: %s', cache_key)
            persisted_state_cache[cache_key] = new_state


def fetch(datadir):
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
        logger.debug('Moving tmp file from %s to %s', filepath, epoch_path)
        shutil.move(filepath, epoch_path)
        logger.debug('Downloaded original directly to file: %s', epoch_path)
    else:
        # get the bleeding edge (changes in the last minute)
        filepath, http_message = urllib.urlretrieve(url)
        current_state = json.load(open(filepath))

        # load beginning-of-day patches
        started = time.time()
        logger.info('Persisting new state to epoch-patches pair: %s, %s', epoch_path, patches_path)
        persist_new_state(epoch_path, patches_path, current_state)
        ended = time.time()
        logger.info('Finished persisting new state in %0.2f seconds.', ended - started)
