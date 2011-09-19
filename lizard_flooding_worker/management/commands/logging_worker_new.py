#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.management.base import BaseCommand
from lizard_flooding_worker.client.worker.worker import Worker
from lizard_flooding_worker.client.worker.action_logging import ActionLogging
from lizard_flooding_worker.client.worker.broker_connection import BrokerConnection

import logging
log = logging.getLogger("lizard-flooding.management.logging_worker")


class Command(BaseCommand):
    """
    Run logging worker. The worker listens to logging
    queue, retrieves the messages and insert they
    into storage.
    """
    def handle(self, *args, **options):
        task_code = "logging"
        if len(args) > 0:
            task_code = args[0]

        broker = BrokerConnection()
        connection = broker.connect_to_broker()

        if connection is None:
            log.error("Could not connect to broker.")
            return

        action = ActionLogging()

        logging_worker = Worker(connection, task_code, action)
        logging_worker.run_worker()
