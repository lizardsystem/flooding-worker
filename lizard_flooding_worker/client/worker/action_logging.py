#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson
from datetime import datetime

from lizard_flooding_worker.models import Customer
from lizard_flooding_worker.models import Scenario
from lizard_flooding_worker.models import Task
from lizard_flooding_worker.models import Logging

from action import Action

import logging
log = logging.getLogger('lizard-flooding.action_logging')


class ActionLogging(Action):

    def callback(self, ch, method, properties, body):
        """
        Inserts logging data into database.
        Used by logging_worker.
        """
        body_dict = simplejson.loads(body)
        try:
            new_logging = Logging(
                customer=Customer.objects.get(pk=body_dict["customer_id"]),
                scenario=Scenario.objects.get(pk=body_dict["scenario_id"]),
                task=Task.objects.all().filter(
                    scenario=body_dict["scenario_id"]).filter(
                    code=body_dict["curr_task_code"])[0],
                    time=datetime.utcfromtimestamp(body_dict["event_time"]),
                level=body_dict["curr_log_level"],
                message=body_dict["message"])
            new_logging.save()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            log.error("Could not write logging message into database: %s" % ex)
