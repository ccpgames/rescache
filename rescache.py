import sys

import progress

from move import move_cache
from parse_index import parse_index

from paths import get_shared_cache_folder, get_res_folder
from diff import diff_cache

from verify import verify_cache
from purge import purge_cache
from download import download_cache


COMMAND_HELP_STRING = """
rescache is a tool for verifying and managing the EVE shared resource cache.

The following commands are available:

  verify                    Verifies the contents of files in the rescache
  download                  Downloads any missing files
  purge                     Purges extra files from the rescache
  move <new_location>       Moves the rescache to a new location
  diff                      Shows statistics on missing/extra files

"""


def verify_command():
    try:
        with open("resfileindex.txt") as f:
            index = parse_index(f)
        verify_cache(index, get_res_folder())
    except IOError:
        print "Couldn't open resfileindex.txt"
        sys.exit(1)


def diff_command():
    try:
        with open("resfileindex.txt") as f:
            index = parse_index(f)
        diff_cache(index, get_res_folder())
    except IOError:
        print "Couldn't open resfileindex.txt"
        sys.exit(1)


def purge_command():
    try:
        with open("resfileindex.txt") as f:
            index = parse_index(f)
        purge_cache(index, get_res_folder())
    except IOError:
        print "Couldn't open resfileindex.txt"
        sys.exit(1)


def download_command():
    try:
        with open("resfileindex.txt") as f:
            index = parse_index(f)
        download_cache(index, get_res_folder())
    except IOError:
        print "Couldn't open resfileindex.txt"
        sys.exit(1)


def move_command(new_path):
    move_cache(get_shared_cache_folder(), new_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print COMMAND_HELP_STRING
        print "The current shared cache location is\n\n\t%s" % get_shared_cache_folder()
        sys.exit()

    progress.stream = sys.stdout

    command = sys.argv[1]

    try:
        if command == "verify":
            verify_command()
        elif command == "diff":
            diff_command()
        elif command == "purge":
            purge_command()
        elif command == "download":
            download_command()
        elif command == "move":
            if len(sys.argv) < 3:
                print "Missing argument for new location"
                sys.exit(1)

            dest = sys.argv[2]
            move_command(dest)

    except KeyboardInterrupt:
        progress.clear()
        print "Operation cancelled"
        sys.exit(1)