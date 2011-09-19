#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from django.core.management.base import BaseCommand
from lizard_flooding_worker.client.worker.action_scenario import ActionScenario
from lizard_flooding_worker.client.worker.broker_connection import BrokerConnection
from lizard_flooding_worker.client.worker.message_logging_handler import AMQPMessageHandler

import logging
log = logging.getLogger("lizard-flooding.management.start_scenaro")

class Command(BaseCommand):

    def handle(self, *args, **options):
        scenario_id = None
        numeric_level = 10  # DEBUG

        if len(args) > 0:
            scenario_id = args[0]
        else:
           log.error("NOT STARTED: Expected scenario id as argument.")
           return

        if len(args) > 1:
            numeric_level = getattr(logging, args[1], None)
            if not isinstance(numeric_level, int):
                raise ValueError("Invalid log level: %s" % args[1])
            log.info("Worker wil start in %s mode." % args[1])
        else:
            log.info("Worker wil start in DEBUG mode.")

        broker = BrokerConnection()
        connection = broker.connect_to_broker()

        if connection is None:
            log.error("Could not connect to broker.")
            return

        action = ActionScenario(connection, scenario_id)

        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_handler = logging.handlers.AMQPMessageHandler(action)
        broker_handler.setLevel(numeric_level)

        action.set_broker_logging_handler(broker_handler)

        action.start_scenario("120")
        connection.close()
