#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from flooding_worker.models import Workflow
from flooding_worker.models import WorkflowTask
from flooding_worker.models import WorkflowTemplate
from flooding_worker.models import WorkflowTemplateTask
from flooding_worker.worker.action import Action
from flooding_lib.models import Scenario

from pika import BasicProperties

import time
import logging


class ActionWorkflow(Action):

    def __init__(self, connection, scenario_id):
        self.connection = connection
        self.log = logging.getLogger('flooding.action.workflow')
        self.scenario_id = scenario_id
        self.body = {}
        self.workflow = None
        self.bulk_tasks = []
        self.channel = self.connection.channel()

    def callback(self, ch, method, properties, body):
        pass

    def perform_workflow(self):
        """
        Creates workflow and tasks.
        Creates message body as instruction
        Sends message to next queue(s)
        """
        self.create_workflow()
        self.body = self.retrieve_workflow_options()
        self.set_message_properties()
        self.start_workflow()


    def create_workflow(self):
        """
        Creates and sets workflow, tasks.
        """
        try:
            scenario = Scenario.objects.get(pk=self.scenario_id)
            template = WorkflowTemplate.objects.get(pk=scenario.workflow_template_id)
            template_tasks = WorkflowTemplateTask.objects.filter(workflow_template=template.id)
            self.workflow = Workflow(scenario=scenario,
                                     code=self.scenario_id,
                                     priority=scenario.calcpriority)
            self.workflow.save()
            self.bulk_tasks = []
            for template_task in template_tasks:
                task = WorkflowTask(workflow=self.workflow,
                                    code=template_task.code,
                                    sequence=template_task.sequence,
                                    max_failures=template_task.max_failures,
                                    max_duration_minutes=template_task.max_duration_minutes)
                task.save()
                self.bulk_tasks.append(task)
        except Exception as ex:
            self.log.error("{0}".format(ex))


    def retrieve_workflow_options(self):
        """
        Creates a body as instruction mechanizm
        for messaging.
        """
        option = {}
        instruction = {}
        workflow_tasks = {}
        task_failures = {}

        for task in self.bulk_tasks:
            if task.sequence == 0:
                option["curr_task_code"] = task.code.name
            instruction[task.code.name] = task.sequence
            workflow_tasks[task.code.name] = task.id
            task_failures[task.code.name] = task.max_failures

        option["instruction"] = instruction
        option["workflow_tasks"] = workflow_tasks
        option["max_failures"] = task_failures
        option["max_failures_tmp"] = task_failures
        if self.workflow:
            option["workflow_id"] = self.workflow.id
            option["priority"] = self.workflow.priority
        option["scenario_id"] = self.scenario_id
        option["curr_log_level"] = ""
        option["message"] = ""
        option["event_time"] = ""
        option["next_sequence"] = 0
        return option

    def start_workflow(self):
        """Sends trigger and logging messages to broker."""
        self.log.info("Start workflow")

        queues = self.next_queues()
        self.increase_sequence()
        for queue in queues:
            self.set_current_task(queue)
            self.send_trigger_message(self.body,
                                 "Message emitted to queue %s" % queue,
                                 queue)

    def set_message_properties(self):
        print type(self.workflow.id)
        self.properties = BasicProperties(content_type="application/json",
                                          delivery_mode=2,
                                          priority=self.workflow.priority,
                                          message_id=str(self.workflow.id),
                                          timestamp=time.time())
