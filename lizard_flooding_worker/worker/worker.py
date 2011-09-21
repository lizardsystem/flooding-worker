#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from pika.exceptions import AMQPChannelError

import logging
log = logging.getLogger('lizard-flooding.worker')


class Worker():

    def __init__(self, connection, task_code, action):
        self.connection = connection
        self.action = action
        self.task_code = task_code

    def run_worker(self):
        """
        Runs common worker.
        Task code equals to queue.
        """
        try:
            channel = self.connection.channel()
            channel.basic_consume(self.action.callback,
                                  queue=self.task_code,
                                  no_ack=False)
            channel.start_consuming()
        except AMQPChannelError as ex:
            log.error(ex)
