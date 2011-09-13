from worker.messaging import run_worker
from worker.brokerconfig import QUEUES

if __name__ == "__main__":
    run_worker(QUEUE["120"])
