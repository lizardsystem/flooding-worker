#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import logging

import messaging


class AMQPMessageHandler(logging.Handler):
    """
    Sends the loggings to message broker.
    """

    def __init__(self, body):
        logging.Handler.__init__(self)
        self.body = body

    def emit(self, record):
        messaging.send_logging_message(self.body, record.msg, record.levelno)
