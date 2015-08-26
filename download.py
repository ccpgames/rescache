import gzip
import os
import urllib2
import threading
import time
import Queue
import StringIO
from checksum import calc_checksum
from format_memory import format_memory

import progress

DOWNLOAD_THREAD_COUNT = 12

def get_url_root():
    return 'http://res.eveonline.ccpgames.com'


def DownloadResourceFile(target_url, expected_checksum, target_path):
    try:
        contents = urllib2.urlopen(target_url)
    except urllib2.URLError:
        return False, "Couldn't open %s" % target_url

    data = contents.read()
    headers = contents.info()
    if ('content-encoding' in headers.keys() and headers['content-encoding']=='gzip'):
        sio = StringIO.StringIO(data)
        gzipper = gzip.GzipFile(fileobj=sio)
        data = gzipper.read()

    temp_path = target_path + ".tmp"

    with open(temp_path, "wb") as f:
        f.write(data)

    checksum_from_file = calc_checksum(temp_path)
    if checksum_from_file != expected_checksum:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        return False, "Checksum didn't match"

    try:
        os.rename(temp_path, target_path)
    except OSError:
        return False, "Failed to rename temp file to final name"

    return True, "OK"


class DownloadThread(threading.Thread):
    def __init__(self, target_folder, file_queue):
        threading.Thread.__init__(self)
        self.target_folder = target_folder
        self.file_queue = file_queue
        self.failed = 0
        self.succeeded = 0
        self.messages = []
        self._stop = False

    def process_file(self, file_entry, target_folder):
        relative_file_path = file_entry.cached_name
        split_file_path = urllib2.posixpath.split(relative_file_path)
        target_path = os.path.join(target_folder, *split_file_path)
        target_url = urllib2.posixpath.join(get_url_root(), *split_file_path)

        if os.path.exists(target_path):
            return

        nested_target_dir = os.path.dirname(target_path)
        if not os.path.exists(nested_target_dir):
            try:
                os.makedirs(nested_target_dir)
            except OSError:
                pass

        status, message = DownloadResourceFile(target_url, file_entry.md5_checksum, target_path)
        if status:
            self.succeeded += 1
        else:
            self.failed += 1
            self.messages.append(message)

    def stop(self):
        self._stop = True

    def run(self):
        try:
            def f_proc_file(f):
                self.process_file(f, self.target_folder)

            while not self._stop:
                try:
                    f_proc_file(self.file_queue.get(timeout=0.1))
                except Queue.Empty:
                    break
        except Exception as e:
            import traceback
            print traceback.format_exc(e)


def download_missing_files(res_folder, files_to_download):
    q = Queue.Queue()
    for f in files_to_download:
        q.put(f)

    downloaded_files = 0
    old_size = q.qsize()
    num_files = len(files_to_download)

    thread_list = []

    for i in range(DOWNLOAD_THREAD_COUNT):
        t = DownloadThread(res_folder, q)
        thread_list.append(t)
        t.start()

    try:
        while not q.empty():
            progress.write("Downloaded %6.1d of %6.1d files\r" % (downloaded_files, num_files))
            new_size = q.qsize()
            d_size = old_size - new_size
            if d_size:
                downloaded_files += d_size
            old_size = new_size
            time.sleep(0.5)

        progress.clear()

        num_failed = 0
        num_succeeded = 0
        for t in thread_list:
            t.join()
            num_failed += t.failed
            num_succeeded += t.succeeded
            if t.messages:
                print t.messages

        return num_succeeded, num_failed

    except KeyboardInterrupt:
        progress.clear()
        print "Stopping download threads"
        for t in thread_list:
            t.stop()
        for t in thread_list:
            t.join()
        raise

def scan_missing_files(index, res_folder):
    num_files = len(index)
    missing = 0
    scanned = 0
    missing_files = []
    missing_bytes = 0
    missing_bytes_on_disk = 0
    for entry in index:
        scanned += 1
        progress.write("%6.1d of %6.1d files (%6.1d missing - %10.10s - %10.10s on disk)\r" %
                       (scanned, num_files, missing, format_memory(missing_bytes), format_memory(missing_bytes_on_disk)))
        filename = os.path.join(res_folder, entry.cached_name)
        if not os.path.exists(filename):
            missing += 1
            missing_files.append(entry)
            missing_bytes += entry.compressed_size
            missing_bytes_on_disk += entry.size_in_bytes

    progress.clear()
    print "%6.1d files missing - %10.10s - %10.10s on disk\r" % \
          (missing, format_memory(missing_bytes), format_memory(missing_bytes_on_disk))
    print

    return missing_files


def download_cache(index, res_folder):
    missing_files = scan_missing_files(index, res_folder)
    num_succeeded, num_failed = download_missing_files(res_folder, missing_files)
    print "Downloaded %d files (%d failed)" % (num_succeeded, num_failed)

