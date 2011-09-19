#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from pika import BlockingConnection
from pika import ConnectionParameters
from pika import PlainCredentials

from brokerconfig import CONNECT_SETTINGS

import logging
log = logging.getLogger('lizard-flooding.broker')


class BrokerConnection(object):

    def __init__(self):
        self.host = CONNECT_SETTINGS["BROKER_HOST"]
        self.port = CONNECT_SETTINGS["BROKER_PORT"]
        self.virtual_host = CONNECT_SETTINGS["BROKER_VHOST"]
        self.user = CONNECT_SETTINGS["BROKER_USER"]
        self.password = CONNECT_SETTINGS["BROKER_PASSWORD"]

    def connect_to_broker(self):
        """Returns connection object,
        """
        credentials = PlainCredentials(self.user, self.password)
        parameters = ConnectionParameters(host=self.host,
                                          port=self.port,
                                          virtual_host=self.virtual_host,
                                          credentials=credentials)
        connection = BlockingConnection(parameters)
        return connection
