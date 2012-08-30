#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import time
import simplejson

from django.conf import settings
from flooding_worker.worker.messaging_body import Body


class Action(object):

    CREATED = u'CREATED'
    QUEUED = u'QUEUED'
    STARTED = u'STARTED'
    SUCCESS = u'SUCCESS'
    FAILED = u'FAILED'

    ALIVE = u'ALIVE'
    DOWN = u'DOWN'
    BUSY = u'BUSY'

    def __init__(self):
        self.body = None
        self.broker_logging_handler = None
        self.channel = None
        self.properties = None

    def callback(self, ch, method, properties, body):
        """worker callback function"""
        raise NotImplementedError("Should have implemented this")

    def send_logging_message(self, message, log_level="0"):
        self.set_logging_to_body(message, log_level)
        queue_options = self.retrieve_queue_options("logging")
        self.publish_message(self.channel, queue_options, self.body)

    def send_trigger_message(self, body, message, queue):
        queue_options = self.retrieve_queue_options(queue)
        self.publish_message(self.channel, queue_options, body)

    def publish_message(self, channel, queue_options, body):
        """Sends a message to broker. """
        channel.basic_publish(exchange=queue_options["exchange"],
                              routing_key=queue_options["binding_key"],
                              body=simplejson.dumps(body),
                              properties=self.properties)

    def set_broker_logging_handler(self, handler):
        self.broker_logging_handler = handler
        self.log.addHandler(handler)

    def set_logging_to_body(self, message, log_level="0"):
        """Sets logging info into body."""
        self.body[Body.MESSAGE] = str(message)
        self.body[Body.CURR_LOG_LEVEL] = log_level
        self.body[Body.TIME] = time.time()

    def retrieve_queue_options(self, task_code):
        """Retrieves queue info from brokerconfig file."""
        return settings.QUEUES.get(task_code, None)

    def root_queues(self):
        """Retrieve root queues from task's body."""
        instruction = self.body[Body.INSTRUCTION]
        return [queue_code for queue_code, parent_code in instruction.iteritems()
                if queue_code == parent_code]

    def next_queues(self):
        """
        Recovers queue(s) of next task(s)
        by increasing the sequence.
        """
        instruction = self.body[Body.INSTRUCTION]
        current_queue = self.body[Body.CURR_TASK_CODE]
        return [queue_code for queue_code, parent_code in instruction.iteritems()
                if queue_code != parent_code and current_queue == parent_code]

    def set_current_task(self, queue):
        self.body[Body.CURR_TASK_CODE] = queue

    def set_task_status(self, status):
        self.body[Body.STATUS] = status
