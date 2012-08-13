#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson

from flooding_worker.worker.action import Action
from flooding_worker.worker.action_task import ActionTask
from flooding_worker.worker.worker import WorkerProcess
from flooding_worker.worker.message_logging_handler import AMQPMessageHandler
from multiprocessing import Queue

import logging

WORKER_COMMAND = ('start', 'kill')


class ActionSupervisor(Action):

    def __init__(self, connection, task_code, worker_nr, numeric_loglevel=20):
        self.task_code = task_code
        self.worker_nr = worker_nr
        self.connection = connection
        self.numeric_loglevel = numeric_loglevel
        self.log = logging.getLogger('worker.action_supervisor')
        self.processes = {}

    def callback(self, ch, method, properties, body):
        """
        """
        self.body = simplejson.loads(body)
        self.channel = ch
        self.properties = properties
        self.execute_command()

        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    def execute_command(self):
        command = self.body.get("command", None)
        success = True
        if command == 'start':
            worker_nr = self.next_worker_nr()
            task_code = self.body.get("task_code", None)
            self.log.info("Start worker nr. {0} to performe task {1}".format(
                    worker_nr, task_code))
            # set handler to forward logging to message broker
            action = ActionTask(task_code, worker_nr)
            self.set_logger(action)
            
            # create and start worker as subprocess
            p = WorkerProcess(worker_nr, task_code)
            p.start(action)

            self.processes.update({str(worker_nr): p})
        elif command == 'kill':
            worker_nr = str(self.body.get("worker_nr", None))
            p = self.get_process(worker_nr)
            if p is not None and p.is_alive():
                p.connection.disconnect()
                p.terminate()
                p.join()
                self.processes.pop(worker_nr)
                self.log.info("Worker nr.{0} is closed.".format(worker_nr))
        else:
            self.log.warning("The command '{0}' is NOT defined.")
            success = False
        return success

    def next_worker_nr(self):
        numbers = self.processes.keys()
        numbers.sort()
        if len(numbers) > 0:
            number = int(numbers[-1]) + 1
            return number
        return 1

    def get_process(self, worker_nr):
        p = self.processes.get(worker_nr, None)
        if p is None:
            self.log.error("Worker nr.{0} is not present".format(worker_nr))
        return p

    def set_logger(self, action):
        action.log = logging.getLogger(
            'flooding.action.{0}'.format(action.worker_nr))
        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_logging_handler = logging.handlers.AMQPMessageHandler(
            action, self.numeric_loglevel)
        action.set_broker_logging_handler(broker_logging_handler)
