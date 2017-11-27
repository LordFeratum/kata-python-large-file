from multiprocessing import Process, JoinableQueue, Queue, cpu_count
# from codecs import iterdecode
# from itertools import islice, groupby
from urllib.request import urlopen

from settings import settings


class CSVProcessor(Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._result = dict(rows=0, avg=0)

    def run(self):
        while True:
            task = self._task_queue.get()
            if task.is_eof():
                break

            self._result['rows'] += 1
            self._result['avg'] += task()
            self._task_queue.task_done()

        self._result_queue.put(self._result)
        return


class Task:
    def __init__(self, row, is_eof=False):
        self._row = row.decode('utf-8')
        self._is_eof = is_eof

    def __call__(self):
        return 1

    def is_eof(self):
        return self._is_eof

    def __str__(self):
        return self._row


def process_csv(url, tasks, encoding='utf-8'):
    response = urlopen(url)
    line = response.readline()
    while line:
        tasks.put(Task(line))
        line = response.readline()


def main():
    url = settings['amazon']['url']

    tasks = JoinableQueue()
    results = Queue()

    consumers = [
        CSVProcessor(tasks, results)
        for _ in range(cpu_count() * 2)
    ]
    for consumer in consumers:
        consumer.start()

    process_csv(url, tasks)

    for _ in consumers:
        tasks.put(Task(None, is_eof=True))

    tasks.join()

    while True:
        result = results.get()
        print("RESULT: ", result)


if __name__ == '__main__':
    main()
