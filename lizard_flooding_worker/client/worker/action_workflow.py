#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from lizard_flooding_worker.models import Workflow
from lizard_flooding_worker.models import Task
from lizard_flooding_worker.client.worker.action import Action

import logging


class ActionWorkflow(Action):

    def __init__(self, connection, workflow_id):
        self.connection = connection
        self.log = logging.getLogger('lizard-flooding.action.workflow')
        self.workflow_id = workflow_id
        self.body = self.retrieve_workflow_options()

    def callback(self, ch, method, properties, body):
        pass

    def retrieve_workflow_options(self):
        """Retrieves workflow info from database.
        1 task_code per workflow
        for example:
        wel (120, 130, (160, 132))
        not (120, 120, 130, (160, 132))"""
        tasks = Task.objects.all().filter(workflow=self.workflow_id)
        workflow = Workflow.objects.get(pk=self.workflow_id)
        option = {}
        instruction = {}
        for task in tasks:
            if int(task.sequence) == 1:
                option["curr_task_code"] = task.code
            instruction[task.code] = task.sequence
        option["instruction"] = instruction
        option["customer_id"] = workflow.customer.id
        option["workflow_id"] = self.workflow_id
        option["priority"] = ""
        option["curr_log_level"] = ""
        option["message"] = ""
        option["event_time"] = ""
        option["next_sequence"] = 1
        return option

    def start_workflow(self, task_code):
        """Sends trigger and logging messages to broker."""
        channel = self.connection.channel()
        task_queue_options = self.retrieve_queue_options(task_code)
        self.log.info("Start workflow")
        #send trigger
        #TODO send trigger on the smae way as by action_task
        self.publish_message(channel, task_queue_options, self.body)
        self.log.info("Started workflow")
        #self.connection.close()
