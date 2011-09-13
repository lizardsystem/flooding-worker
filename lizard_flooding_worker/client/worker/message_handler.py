#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import logging

import messaging


class AMQPMessageHandler(logging.Handler):

    def __init__(self, body):
        logging.Handler.__init__(self)
        self.body = body

    def emit(self, record):
        print type(record.msg).__name__
        print record.levelno
        messaging.send_logging_message(self.body, record.msg, record.levelno)
