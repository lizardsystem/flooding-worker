#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson

from lizard_flooding_worker.worker.action import Action
from lizard_flooding_worker.perform_task import perform_task

import logging


class ActionTask(Action):

    def __init__(self, connection, task_code, worker_nr):
        self.task_code = task_code
        self.worker_nr = worker_nr
        self.connection = connection
        self.body = None
        self.log = logging.getLogger('lizard-flooding.action.task')

    def callback(self, ch, method, properties, body):
        """sends logging to logging queue"""
        self.body = simplejson.loads(body)
        self.log.info("Start task")
        try:
            perform_task(self.body["scenario_id"],
                         int(self.task_code),
                         self.worker_nr,
                         self.broker_logging_handler)
        except Exception as ex:
            self.log.error("{0}".format(ex))
            return

        self.log.info("End task")
        queues = self.next_queues()
        self.increase_sequence()
        for queue in queues:
            self.set_current_task(queue)
            self.send_trigger_message(self.body,
                                 "Message emitted to queue %s" % queue,
                                 queue)
        ch.basic_ack(delivery_tag=method.delivery_tag)
