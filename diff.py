import os

from format_memory import format_memory
import progress


def scan_missing_files(index, res_folder):
    print "Scanning index, checking for missing files"
    num_files = len(index)
    missing = 0
    missing_bytes = 0
    missing_download_bytes = 0
    scanned = 0
    for entry in index:
        scanned += 1
        progress.write("Scanned %6.1d of %6.1d files (%6.1d missing)\r" %
                       (scanned, num_files, missing))
        filename = os.path.join(res_folder, entry.cached_name)
        if not os.path.exists(filename):
            missing += 1
            missing_download_bytes += entry.compressed_size
            missing_bytes += entry.size_in_bytes
            continue
    progress.clear()
    return missing, missing_bytes, missing_download_bytes


def scan_extra_files(index_by_cached_names, res_folder):
    print "Scanning %s, checking for extra files" % res_folder
    extras = 0
    extra_bytes = 0
    scanned = 0
    for root, dirs, files in os.walk(res_folder):
        for name in files:
            scanned += 1
            progress.write("Scanned %7.1d files (%7.1d extra)\r" % (scanned, extras))
            parent_folder = os.path.split(root)[1]
            cached_name = "%s/%s" % (parent_folder, name)
            if cached_name not in index_by_cached_names:
                extras += 1
                full_name = os.path.join(root, name)
                extra_bytes += os.path.getsize(full_name)
    progress.clear()
    return extras, extra_bytes


def diff_cache(index, res_folder):
    index_by_cached_names = {}
    for entry in index:
        index_by_cached_names[entry.cached_name] = entry

    extras, extra_bytes = scan_extra_files(index_by_cached_names, res_folder)
    missing, missing_bytes, missing_download_bytes = scan_missing_files(index, res_folder)

    if missing:
        print "%d files missing:" % missing
        print "%s to download (%s on disk)" % (format_memory(missing_download_bytes), format_memory(missing_bytes))
        print
    else:
        print "No missing files"

    if extras:
        print "%d extra files (%s)" % (extras, format_memory(extra_bytes))
    else:
        print "No extra files"