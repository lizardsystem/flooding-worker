#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import time
import simplejson
import logging

from flooding_worker.worker.brokerconfig import QUEUES


class Action(object):

    def __init__(self):
        self.log = logging.getLogger("flooding.action")
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
        self.body["message"] = message
        self.body["curr_log_level"] = log_level
        self.body["event_time"] = time.time()

    def retrieve_queue_options(self, task_code):
        """Retrieves queue info from brokerconfig file."""
        return QUEUES[task_code]

    def next_queues(self):
        """
        Recovers queues(s) of next task(s)
        by increasing the sequence.
        """
        next_sequence = int(self.body["next_sequence"]) + 1
        instruction = self.body["instruction"]
        queues = []
        for (queue_code, sequence) in instruction.iteritems():
            if int(sequence) == next_sequence:
                queues.append(queue_code)
        return queues

    def increase_sequence(self):
        self.body["next_sequence"] = int(self.body["next_sequence"]) + 1

    def set_current_task(self, queue):
        self.body["curr_task_code"] = queue
