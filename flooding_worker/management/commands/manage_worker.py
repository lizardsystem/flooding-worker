#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from optparse import make_option

from django.core.management.base import BaseCommand
from flooding_worker.file_logging import setFileHandler, removeFileHandlers
from flooding_worker.worker.action_worker import ActionWorker
from flooding_worker.worker.broker_connection import BrokerConnection
from flooding_worker.worker.message_logging_handler import AMQPMessageHandler

import logging
log = logging.getLogger("flooding.management.start_scenario")


class Command(BaseCommand):

    help = ("Example: bin/django start_scenario_new "\
            "--worker_nr 1"\
            "--command stop "\
            "--queue_code 900"\
            "--log_level DEBUG")

    option_list = BaseCommand.option_list + (
            make_option('--log_level',
                        help='logging level 10=debug 50=critical',
                        default='DEBUG',
                        type='str'),
            make_option('--worker_nr',
                        help='number of worker',
                        type='str'),
            make_option('--command',
                        help='command to be executed start/pause/stop',
                        type='str'),
            make_option('--task_code',
                        help='use to start worker for certain task',
                        type='str'),
            make_option('--queue_code',
                        help='queue code to send a message',
                        type='str'))

    def handle(self, *args, **options):
        """
        Open connection to broker.
        Creates message.
        Creates logging handler to send loggings to broker.
        Sets logging handler to ActionWorkflow object.
        Close connection.
        """
        numeric_level = getattr(logging, options["log_level"].upper(), None)
        if not isinstance(numeric_level, int):
            log.error("Invalid log level: %s" % options["log_level"])
            numeric_level = 10

        broker = BrokerConnection()
        connection = broker.connect_to_broker()

        removeFileHandlers()
        setFileHandler('start')

        if connection is None:
            log.error("Could not connect to broker.")
            return

        action = ActionWorker(connection,
                              options["worker_nr"],
                              options["command"],
                              options["task_code"],
                              options["queue_code"])

        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        broker_handler = logging.handlers.AMQPMessageHandler(action,
                                                             numeric_level)

        action.set_broker_logging_handler(broker_handler)
        action.execute()

        if connection.is_open:
            connection.close()
