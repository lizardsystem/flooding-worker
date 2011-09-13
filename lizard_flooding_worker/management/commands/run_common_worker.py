#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.management.base import BaseCommand
from lizard_flooding_worker.client.worker import messaging


class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) > 0:
            messaging.run_worker(args[0])
        else:
            print "Usage: bin/django run_common_worker [queue_name]"
