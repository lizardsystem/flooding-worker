#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from lizard_flooding_worker.models import Scenario
from lizard_flooding_worker.models import Task
from lizard_flooding_worker.client.worker.action import Action

import logging


class ActionScenario(Action):

    def __init__(self, connection, scenario_id):
        self.connection = connection
        self.log = logging.getLogger('lizard-flooding.action.scenario')
        self.scenario_id = scenario_id
        self.body = self.retrieve_scenario_options()

    def callback(self, ch, method, properties, body):
        pass

    def retrieve_scenario_options(self):
        """Retrieves scenario info from database.
        1 task_code per scenario
        for example:
        wel (120, 130, (160, 132))
        not (120, 120, 130, (160, 132))"""
        tasks = Task.objects.all().filter(scenario=self.scenario_id)
        scenario = Scenario.objects.get(pk=self.scenario_id)
        option = {}
        instruction = {}
        for task in tasks:
            if int(task.sequence) == 1:
                option["curr_task_code"] = task.code
            instruction[task.code] = task.sequence
        option["instruction"] = instruction
        option["customer_id"] = scenario.customer.id
        option["scenario_id"] = self.scenario_id
        option["priority"] = ""
        option["curr_log_level"] = ""
        option["message"] = ""
        option["event_time"] = ""
        option["next_sequence"] = 1
        return option

    def start_scenario(self, task_code):
        """Sends trigger and logging messages to broker."""
        channel = self.connection.channel()
        task_queue_options = self.retrieve_queue_options(task_code)
        self.log.info("Start scenario")
        #send trigger
        #TODO send trigger on the smae way as by action_task
        self.publish_message(channel, task_queue_options, self.body)
        self.log.info("Started scenario")
        #self.connection.close()
