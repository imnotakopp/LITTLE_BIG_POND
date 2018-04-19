
from scripts.client import Client
from bson import json_util

if __name__ == "__main__":

    conn = Client()

    # returns the tasks that are scheduled to run
    tasks = conn.aggregate(
        database='SYSTEM',
        file_id='collect'
    )

    if not tasks:
        raise ValueError

    for task in tasks:
        # returns the next available processor to handle the task
        worker = conn.aggregate(
            database='SYSTEM',
            file_id='worker_designation'
        )

        if not worker:
            raise ValueError

        worker = worker.pop(0)

        # add the task to the QUEUE with the association to the processor
        conn.insert(
            db='SYSTEM',
            coll='QUEUE',
            docs={
                "workerId": worker['processor'],
                "taskId": task["_id"],
                "config": task['CONFIG'],
                "occurrence": task["OCCURRENCE"],
                "index": worker['taskIndex']
            }
        )
