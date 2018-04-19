from os import cpu_count
from multiprocessing import Pool

from scripts.client import Client
from scripts.worker import Worker


def work(worker_id):
    print("{} is working".format(worker_id))


if __name__ == "__main__":

    conn = Client()

    workers = conn.aggregate(
        database='SYSTEM',
        file_id='worker_generator'
    )

    if not workers:
        raise ValueError

    if len(workers) > cpu_count():
        raise ValueError

    pool = Pool(processes=len(workers))
    for worker in workers:
        p = pool.Process(target=work, args=[worker['_id']])
        p.start()
        p.join()
