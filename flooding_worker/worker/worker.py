#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from pika.exceptions import AMQPChannelError

import logging
log = logging.getLogger('lizard-flooding.worker')


class Worker():

    def __init__(self, connection, task_code, action, worker_nr=1):
        self.connection = connection
        self.action = action
        self.task_code = task_code
        self.worker_nr = worker_nr

    def run_worker(self):
        """
        Runs common worker to perform flooding tasks.
        Task code equals to queue.
        """
        try:
            channel = self.connection.channel()
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(self.action.callback,
                                  queue=self.task_code,
                                  no_ack=False)
            channel.start_consuming()
        except AMQPChannelError as ex:
            log.error("Worker_nr: %s error: %s" % (self.worker_nr, ex))
