#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.management.base import BaseCommand
from lizard_flooding_worker.client.worker.worker import Worker
from lizard_flooding_worker.client.worker.action_task import ActionTask
from lizard_flooding_worker.client.worker.broker_connection import BrokerConnection
from lizard_flooding_worker.client.worker.message_logging_handler import AMQPMessageHandler

import logging
log = logging.getLogger("lizard-flooding.management.logging_worker")


class Command(BaseCommand):
    """
    Run task worker. The worker listens to certain
    queue, retrieves  message, runs task, sends logging.
    """
    def handle(self, *args, **options):
        task_code = None
        numeric_level = 10  # DEBUG

        if len(args) > 0:
            task_code = args[0]
        else:
            log.error("NOT STARTED - expects scenario_id as argument")
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
        # creates action object
        action = ActionTask(connection, task_code)
        # sets broker logging handler to action object
        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_handler = logging.handlers.AMQPMessageHandler(action)
        broker_handler.setLevel(numeric_level)
        action.set_broker_logging_handler(broker_handler)
        # creates and runs worker
        task_worker = Worker(connection, task_code, action)
        task_worker.run_worker()
