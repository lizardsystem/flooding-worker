#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import time
import simplejson
import logging

from pika import BasicProperties

from brokerconfig import QUEUES


class Action(object):

    def __init__(self):
        self.log = logging.getLogger("lizard-flooding.action")
        self.body = None
        self.broker_logging_handler = None

    def callback(self, ch, method, properties, body):
        """worker callback function"""
        raise NotImplementedError("Should have implemented this")

    def send_logging_message(self, message, log_level="0"):
        channel = self.connection.channel()
        self.set_logging_to_body(message, log_level)
        queue_options = self.retrieve_queue_options("logging")
        self.publish_message(channel, queue_options, self.body)
        #self.connection.close()

    def send_trigger_message(self, body, message, queue):
        channel = self.connection.channel()
        queue_options = self.retrieve_queue_options(queue)
        self.publish_message(channel, queue_options, body)
        #self.connection.close()

    def publish_message(self, channel, queue_options, body, properties=None):
        """Sends a message to broker. """
        properties = BasicProperties(content_type="application/json",
                                     delivery_mode=2)
        channel.basic_publish(exchange=queue_options["exchange"],
                              routing_key=queue_options["binding_key"],
                              body=simplejson.dumps(body),
                              properties=properties)

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
