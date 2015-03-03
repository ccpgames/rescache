import os
import urllib2
import threading
import time
import Queue

import progress

DOWNLOAD_THREAD_MAX = 12
DOWNLOAD_THREAD_MIN = 2


def get_url_root():
    return 'http://res.eveonline.ccpgames.com'


def DownloadResourceFile(target_url, target_path):
    contents = urllib2.urlopen(target_url)
    with open(target_path, "wb") as f:
        f.write(contents.read())

class DownloadThread(threading.Thread):
    def __init__(self, target_folder, file_queue):
        threading.Thread.__init__(self)
        self.target_folder = target_folder
        self.file_queue = file_queue
        self.download_total = None
        self._stop = False

    def process_file(self, relative_file_path, target_folder):
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
        DownloadResourceFile(target_url, target_path)

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


def should_use_minimal_threadcount():
    return False


def get_desired_download_thread_count():
    now = time.time()
    if now - get_desired_download_thread_count.last_check < 1.0:
        return get_desired_download_thread_count.last_count
    get_desired_download_thread_count.last_count = DOWNLOAD_THREAD_MAX
    get_desired_download_thread_count.last_check = now
    return get_desired_download_thread_count.last_count
get_desired_download_thread_count.last_check = 0
get_desired_download_thread_count.last_count = 0


def resize_thread_list(res_folder, thread_list, file_queue):
    no_current_threads = len(thread_list)
    desired_no_threads = get_desired_download_thread_count()
    while no_current_threads > desired_no_threads:
        t = thread_list.pop()
        t.stop()
        t.join()
        no_current_threads -= 1
    while no_current_threads < desired_no_threads:
        t = DownloadThread(res_folder, file_queue)
        thread_list.append(t)
        t.start()
        no_current_threads += 1


def download_missing_files(res_folder, files_to_download):
    q = Queue.Queue()
    for f in files_to_download:
        q.put(f)

    thread_list = []

    downloaded_files = 0
    old_size = q.qsize()
    num_files = len(files_to_download)

    try:
        while not q.empty():
            progress.write("Downloaded %6.1d of %6.1d files\r" % (downloaded_files, num_files))
            new_size = q.qsize()
            d_size = old_size - new_size
            if d_size:
                downloaded_files += d_size
            old_size = new_size
            resize_thread_list(res_folder, thread_list, q)

        for t in thread_list:
            t.join()

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
    for entry in index:
        scanned += 1
        progress.write("Scanned %6.1d of %6.1d files (%6.1d missing)\r" %
                       (scanned, num_files, missing))
        filename = os.path.join(res_folder, entry.cached_name)
        if not os.path.exists(filename):
            missing += 1
            missing_files.append(entry.cached_name)

    progress.clear()
    return missing_files


def download_cache(index, res_folder):
    missing_files = scan_missing_files(index, res_folder)
    download_missing_files(res_folder, missing_files)

