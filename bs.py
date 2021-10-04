import os
import queue
import sys
import threading
import time

MAX_THREADS = 500
MIN_TASKS_IN_ONE_THREAD = 256


def find_referenced_file(root, target, suffix):
    paths = queue.Queue()
    path_count = 0
    for root, dirs, files in os.walk(root):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(suffix):
                paths.put(path)
                path_count += 1

    class SearchingThread(threading.Thread):
        def __init__(self, work_queue):
            threading.Thread.__init__(self)
            self.work_queue = work_queue
            self.results = []

        def run(self):
            while not self.work_queue.empty():
                path = self.work_queue.get()
                with open(path) as file:
                    content = file.read()
                    if target in content:
                        self.results.append(path)

    threads = []
    work_queue_max_size = max(path_count // (MAX_THREADS - 1), MIN_TASKS_IN_ONE_THREAD)
    while not paths.empty():
        work_queue = queue.Queue(work_queue_max_size)
        pushed = 0
        while not paths.empty() and pushed < work_queue_max_size:
            work_queue.put(paths.get())
            pushed += 1
        thread = SearchingThread(work_queue)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    results = []
    for thread in threads:
        results += thread.results
    return results


def main():
    if len(sys.argv) < 4:
        print("Usage: python bs.py <directory> <target> <suffix>.")
        return
    params = sys.argv[1:]
    dir = params[0]
    if not os.path.isdir(dir):
        print("Error: {0} is not a directory.".format(dir))
        return
    target = params[1]
    suffix = params[2]
    print("Searching...")
    start_time = time.time()
    results = find_referenced_file(dir, target, suffix)
    if len(results) > 0:
        print("Found {0} results in {1} seconds:".format(len(results), time.time() - start_time))
    else:
        print("No results found.")
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
