"""Module with utility functions to deal with music files"""

import re
import os
import itertools

FILE_TYPES = ('aif', 'mp3')

PATH_REPLACMENTS = {
    '[\*\?\|:"<>]': '',
    '[\x00-\x1f]':  '_',
    '[\\\\/]': '-',
    '\.$':     '',
    '^\.':     '',
    '\s+$':    '',
    '^\s+':    '',
}

def determine_path(track):
    """Determine the filename and path of a track based on it's tags"""

    path_components = []
    name_components = []

    ### Construct track directory names
    #
    # {publisher}/[{catalog_number}] {album}/Disc {disc}/
    #
    #  - If publisher is None: '[+no-label]'
    #  - If album and catalog_number is None: '[+singles]'
    #  - Disc component not required if there is only 1 disc
    #

    # First directory is the publisher
    path_components.append(track.publisher or '[+no-label]')

    # Second directory is the album name and catalog number
    if track.album and track.catalog_id:
        path_components.append('[{}] {}'.format(track.catalog_id, track.album))
    elif track.album and not track.catalog_id:
        path_components.append('[--] {}'.format(track.album))
    else:
        path_components.append(track.album or '[+singles]')

    # If the album has multiple discs include them as a directory
    if track.disc.total > 1:
        path_components.append('Disc {}'.format(track.disc.number))

    ### Construct track filename
    #
    # {track.number}. [{catalog_id}] [{initial_key}] {artist} - {title}
    #
    #  - Exclude track number (and trailing dot) if track is a single
    #  - Exclude initial key (with enclosing brackets) unless available
    #  - Exclude catalog number (with enclosing brackets) if track is a single
    #

    # If part of an album or EP include the track number
    if track.album and track.track.number:
        name_components.append('{0:02}.'.format(track.track.number))

    # If this track is a single and has a catalog number include it
    if not track.album and track.catalog_id:
        name_components.append('[{}]'.format(track.catalog_id))

    # Include initial key of the track if available
    name_components.append('[{}]'.format(track.initial_key or '--'))

    # Finally artist and title of the track
    name_components.append('{} - {}'.format(track.artist, track.title))

    ### Construct the logical path
    path_components.append(' '.join(name_components))

    # Remove special characters from components
    for p, r in PATH_REPLACMENTS.iteritems():
        path_components = [re.sub(p, r, c) for c in path_components]

    # Convert to full path
    return os.path.join(*path_components) + os.path.splitext(track.file_path)[1]

def collect_files(paths, recursive=False):
    """Collect paths to all supported media files given a list of directories"""
    types = FILE_TYPES
    files = set()

    assert isinstance(paths, list)

    # Add files given as paths directly to the fileset
    files.update([os.path.realpath(f) for f in paths
        if os.path.isfile(f) and f.endswith(types)])

    # Setup directory walk generators for each path
    walkers = [os.walk(d) for d in paths if os.path.isdir(d)]

    # Combine all generators into one when we want to recursively walk,
    # otherwise just take the first directory for each generator
    if recursive:
        walkers = itertools.chain(*walkers)
    else:
        walkers = map(next, walkers)

    # Add all files into a list
    for root, dirnames, filenames in walkers:
        files.update([os.path.join(root, f) for f in filenames if f.endswith(types)])

    return list(sorted(files))