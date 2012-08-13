#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from pika.exceptions import AMQPChannelError

import logging
log = logging.getLogger('flooding.worker')

from multiprocessing import Process
from flooding_worker.worker.broker_connection import BrokerConnection


def start_action(action):
    action.callback


def set_connection():
    return BrokerConnection().connect_to_broker()


def set_channel(connection):
    try:
        return connection.channel()
    except AMQPChannelError as ex:
        log.error("Worker_nr: {0} error: {1}".format(
                self.worker_nr, ",".join(map(str, ex.args))))


class Worker():

    def __init__(self, connection, task_code, action, worker_nr=1):
        self.connection = connection
        self.action = action
        self.task_code = task_code
        self.worker_nr = worker_nr
        self.channel = None

    def run_worker(self):
        """
        Runs common worker to perform flooding tasks.
        Task code equals to queue's name.
        """
        try:
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(self.action.callback,
                                  queue=self.task_code,
                                  no_ack=False)
            self.channel.start_consuming()
        except AMQPChannelError as ex:
            log.error("Worker_nr: {0} error: {1}".format(
                    self.worker_nr, ",".join(map(str, ex.args))))

    def start_consuming(self):
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()


class WorkerProcess(Process):

    def __init__(self, worker_nr, task_code, *args, **kwargs):
        self.worker_nr = worker_nr
        self.task_code = task_code
        self.connection = None
        self.channel = None
        #self.action = action
        #self.set_connection()
        #self.set_channel()        
        Process.__init__(self, *args, **kwargs)

    # def set_connection(self):
    #     self.connection = BrokerConnection().connect_to_broker()

    # def set_channel(self):
    #     try:
    #         self.channel = self.connection.channel()
    #     except AMQPChannelError as ex:
    #         log.error("Worker_nr: {0} error: {1}".format(
    #                 self.worker_nr, ",".join(map(str, ex.args))))

    # def set_action(self, action):
    #     self.action = action

    def run(self, action):
        try:
            self.action = action
            self.connection = set_connection()
            self.channel = set_channel(self.connection) 
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(start_action(self.action),
                                  queue=self.task_code,
                                  no_ack=False)
            self.channel.start_consuming()
        except AMQPChannelError as ex:
            log.error("Worker_nr: {0} error: {1}".format(
                    self.worker_nr, ",".join(map(str, ex.args))))
