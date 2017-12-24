from multiprocessing import Pool
import os

def thread(jobs, selector):
    """
    threads the selector into the number of available processes with a list of jobs as arguments
    :param jobs:
    :param selector:
    :return:
    """
    jobs = chunk(jobs, os.cpu_count())
    pool = Pool(processes=os.cpu_count())
    for job in jobs:
        p = pool.Process(target=selector, args=[job])
        p.start()
        p.join()


def chunk(items, parts):
    """
    breaks a list of items into a specified number of parts.
    :param items: a list of objects to break into chunks
    :param parts: number of process to chunk the jobs into
    :return:
    """
    mod = len(items) % parts
    return [items[x: x + mod] for x in range(0, len(items), mod)]


def test_func(args):
    """
    use this as an example when writing a selector for multithreading
    :param args: a list of elements
    :return:
    """
    if hasattr(os, 'getppid'):
        print("parent process: ", os.getppid())
    print("process id: ", os.getpid())
    print([arg for arg in args])


if __name__ == "__main__":
    tests = [x for x in range(11)]
    thread(tests, test_func)
