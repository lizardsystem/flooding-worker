#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.management.base import BaseCommand
from lizard_flooding_worker.client.worker.messaging import run_logging_worker


class Command(BaseCommand):
    def handle(self, *args, **options):
        queue_code = "logging"
        if len(args) > 0:
            queue_code = args[0]
        run_logging_worker(queue_code)

