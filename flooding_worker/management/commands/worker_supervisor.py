#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from optparse import make_option

from django.core.management.base import BaseCommand
from flooding_worker.file_logging import setFileHandler, removeFileHandlers
from flooding_worker.file_logging import setLevelToAllHandlers
from flooding_worker.worker.worker import Worker
from flooding_worker.worker.action_supervisor import ActionSupervisor
from flooding_worker.worker.broker_connection import BrokerConnection
from flooding_worker.worker.message_logging_handler import AMQPMessageHandler

import logging
log = logging.getLogger("flooding.management.logging_worker")


class Command(BaseCommand):
    """
    Run task worker. The worker listens to certain
    queue, retrieves  message, runs task, sends logging.
    """

    help = ("Example: bin/django task_worker_new "\
            "--task_code 120 "\
            "--log_level DEBUG "\
            "--worker_nr 1")

    option_list = BaseCommand.option_list + (
        make_option('--task_code',
                    help='task that worker must perform',
                    type='str'),
        make_option('--log_level',
                    help='logging level',
                    type='str',
                    default='DEBUG'),
        make_option('--worker_nr',
                    help='use this if you need more than one '\
                    'uitvoerder on this workstation',
                    type='int',
                    default=1000))

    def handle(self, *args, **options):

        if not options["task_code"]:
            log.error("Expected a task_code argument, use --help.")
            return

        numeric_level = getattr(logging, options["log_level"].upper(), None)
        if not isinstance(numeric_level, int):
            log.error("Invalid log level: %s" % options["log_level"])
            numeric_level = 10

        broker = BrokerConnection()
        connection = broker.connect_to_broker()

        removeFileHandlers()
        setFileHandler(options["worker_nr"])
        setLevelToAllHandlers(numeric_level)

        if connection is None:
            log.error("Could not connect to broker.")
            return

        action = ActionSupervisor(connection,
                                  options["task_code"],
                                  options["worker_nr"],
                                  numeric_level)

        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_logging_handler = logging.handlers.AMQPMessageHandler(
            action, numeric_level)
        action.set_broker_logging_handler(broker_logging_handler)

        task_worker = Worker(connection,
                             options["task_code"],
                             action,
                             options["worker_nr"])
        task_worker.run_worker()
        removeFileHandlers()
