import os
import shutil
import sys
from paths import set_shared_cache_folder


def move_cache(src, dest):
    if os.path.exists(dest):
        if os.path.isfile(dest):
            print "'%s' exists as a file - can't move SharedCache folder" % dest
            sys.exit(1)

        print "'%s' already exists - can't move SharedCache folder" % dest
        sys.exit(1)

    try:
        shutil.move(src, dest)
    except (IOError, OSError):
        pass

    set_shared_cache_folder(dest)

    print "SharedCache location has been moved to '%s'" % dest