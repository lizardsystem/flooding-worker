#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from django.core.management.base import BaseCommand
from lizard_flooding_worker.client.worker.messaging import start_scenario


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_scenario(1, "120")
