#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from optparse import make_option

from django.core.management.base import BaseCommand
from flooding_worker.file_logging import setFileHandler, removeFileHandlers
from flooding_worker.worker.worker import Worker
from flooding_worker.worker.action_logging import ActionLogging
from flooding_worker.worker.broker_connection import BrokerConnection

import logging
log = logging.getLogger("flooding.management.logging_worker")


class Command(BaseCommand):
    """
    Run logging worker. The worker listens to logging
    queue, retrieves the messages and insert they
    into storage.
    """

    help = ("Example: bin/django task_worker_new "\
            "--task_code logging ")

    option_list = BaseCommand.option_list + (
        make_option('--task_code',
                    help='tasks that worker must perform',
                    type='str',
                    default='logging'),)

    def handle(self, *args, **options):

        broker = BrokerConnection()
        connection = broker.connect_to_broker()

        removeFileHandlers()
        setFileHandler('logging')

        if connection is None:
            log.error("Could not connect to broker.")
            return

        action = ActionLogging()

        logging_worker = Worker(connection,
                                options["task_code"],
                                action)
        logging_worker.run_worker()
