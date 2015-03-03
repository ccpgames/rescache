import os
import progress

def delete_extra_files(index_by_cached_names, res_folder):
    extras = 0
    scanned = 0
    extra_files = []
    for root, dirs, files in os.walk(res_folder):
        for name in files:
            scanned += 1
            progress.write("Scanned %7.1d files (%7.1d extra)\r" % (scanned, extras))
            parent_folder = os.path.split(root)[1]
            cached_name = "%s/%s" % (parent_folder, name)
            if cached_name not in index_by_cached_names:
                extras += 1
                extra_files.append(os.path.join(root, name))
    progress.clear()

    removed = 0
    for filename in extra_files:
        try:
            progress.write("Removed %7.1d of %7.1d files\r" % (removed, extras))
            os.remove(filename)
            removed += 1
        except IOError:
            pass

    return extras


def purge_cache(index, res_folder):
    index_by_cached_names = {}
    for entry in index:
        index_by_cached_names[entry.cached_name] = entry

    extras = delete_extra_files(index_by_cached_names, res_folder)

    print "Deleted %6.1d extra files from cache folder" % extras