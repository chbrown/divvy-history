import os
import json
import logging
from jsonpatch import JsonPatch

default_logger = logging.getLogger(__name__)


def merge_epoch_and_patches(epoch_path, patches_path, logger=default_logger):
    # read the 0-day (original) file
    with open(epoch_path) as epoch_fp:
        obj = json.load(epoch_fp)

    # apply patches, one by one
    patch_index = 0
    if os.path.exists(patches_path):
        with open(patches_path) as patches_fp:
            for patch_index, patch_line in enumerate(patches_fp):
                patch = JsonPatch.from_string(patch_line)
                patch.apply(obj, in_place=True)

    logger.info('Read %d patches from %s and applied them to %s', patch_index, patches_path, epoch_path)

    return obj


def persist_new_state(epoch_path, patches_path, new_state, logger=default_logger, persisted_state_cache=None):
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
            logger.info('Cache miss (%s), loading from epoch-patches pair: %s, %s', cache_key, epoch_path, patches_path)
            persisted_state = merge_epoch_and_patches(epoch_path, patches_path, logger=logger)
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
