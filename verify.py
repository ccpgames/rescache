import operator
import os
from checksum import calc_checksum
import progress

__author__ = 'snorri.sturluson'


def verify_cache(index, res_folder):
    num_files = len(index)

    missing = 0
    corrupt = 0
    scanned = 0
    for entry in index:
        scanned += 1
        progress.write("Scanned %6.1d of %6.1d files (%6.1d corrupt, %6.1d missing)\r" %
                       (scanned, num_files, corrupt, missing))
        filename = os.path.join(res_folder, entry.cached_name)
        if not os.path.exists(filename):
            missing += 1
            continue

        checksum = calc_checksum(filename)
        if checksum != entry.md5_checksum:
            corrupt += 1
            try:
                os.remove(filename)
            except IOError:
                pass

    progress.clear()
    print "Verified %d files:" % num_files
    print "  %6.1d files corrupt" % corrupt
    print "  %6.1d files not yet downloaded" % missing

    return corrupt, missing
