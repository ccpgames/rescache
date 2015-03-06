import argparse
import os
import sys

import progress

from move import move_cache
from parse_index import parse_index

from paths import get_shared_cache_folder
from diff import diff_cache

from verify import verify_cache
from purge import purge_cache
from download import download_cache


COMMAND_HELP_STRING = """
rescache is a tool for verifying and managing the EVE shared resource cache.

Run with -h (or --help) for help.
"""


def _get_index(args):
    try:
        with open(args.index) as f:
            index = parse_index(f)
    except IOError:
        print "Couldn't open index file: %s" % args.index
        sys.exit(1)
    return index


def _get_res_folder(args):
    if not args.cache:
        print "Shared cache folder location has not been set"
        sys.exit(1)
    return os.path.join(args.cache, "ResFiles")


def verify_command(args):
    verify_cache(_get_index(args), _get_res_folder(args))


def diff_command(args):
    diff_cache(_get_index(args), _get_res_folder(args))


def purge_command(args):
    purge_cache(_get_index(args), _get_res_folder(args))


def download_command(args):
    download_cache(_get_index(args), _get_res_folder(args))


def move_command(args):
    move_cache(args.cache, args.destination)


def main():
    if len(sys.argv) < 2:
        print COMMAND_HELP_STRING
        print "The current shared cache location is\n\n\t%s" % get_shared_cache_folder()
        sys.exit()

    progress.stream = sys.stdout

    parser = argparse.ArgumentParser(
        description="rescache is a tool for verifying and managing the EVE shared resource cache."
    )
    parser.add_argument(
        "-i", "--index",
        default="resfileindex.txt",
        help="The name of an index file to use - defaults to resfileindex.txt"
    )
    parser.add_argument(
        "-c", "--cache",
        default=get_shared_cache_folder(),
        help="The location of the shared cache to use - defaults to what the EVE client uses"
    )
    subparsers = parser.add_subparsers()

    parser_verify = subparsers.add_parser("verify")
    parser_verify.set_defaults(func=verify_command)

    parser_diff = subparsers.add_parser("diff")
    parser_diff.set_defaults(func=diff_command)

    parser_purge = subparsers.add_parser("purge")
    parser_purge.set_defaults(func=purge_command)

    parser_download = subparsers.add_parser("download")
    parser_download.set_defaults(func=download_command)

    parser_move = subparsers.add_parser("move")
    parser_move.add_argument(
        "destination",
        help="The name of the cache folder. This folder must not exist already."
    )
    parser_move.set_defaults(func=move_command)

    args = parser.parse_args()

    try:
        args.func(args)

    except KeyboardInterrupt:
        progress.clear()
        print "Operation cancelled"
        sys.exit(1)


if __name__ == "__main__":
    main()