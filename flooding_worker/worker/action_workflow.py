#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

from flooding_worker.models import Workflow
from flooding_worker.models import WorkflowTask
from flooding_worker.models import WorkflowTemplate
from flooding_worker.models import WorkflowTemplateTask
from flooding_worker.worker.action import Action

from pika import BasicProperties

import time
import logging


class ActionWorkflow(Action):

    def __init__(self, connection, scenario_id, workflowtemplate_id, workflowpriority=0, worker_nr="999"):
        self.connection = connection
        self.log = logging.getLogger('flooding.action.workflow')
        self.scenario_id = scenario_id
        self.workflowtemplate_id = workflowtemplate_id
        self.workflowpriority = workflowpriority
        self.body = {}
        self.workflow = None
        self.bulk_tasks = []
        self.channel = self.connection.channel()
        self.worker_nr = worker_nr

    def callback(self, ch, method, properties, body):
        pass

    def perform_workflow(self):
        """
        Creates workflow and tasks.
        Creates message body as instruction
        Sends message to next queue(s)
        """
        self.set_message_properties()
        if not self.create_workflow():
            self.log.error("Workflow is interrupted.")
            return
        self.body = self.retrieve_workflow_options()
        self.set_message_properties()
        self.start_workflow()


    def create_workflow(self):
        """
        Creates and sets workflow, tasks.
        """
        try:
            template = WorkflowTemplate.objects.get(pk=self.workflowtemplate_id)
            if template is None:
                self.log.warning("Workflow template '%s' does not exist.")
                return False
            template_tasks = WorkflowTemplateTask.objects.filter(workflow_template=template.id)
            if template_tasks.exists() == False:
                self.log.warning("Workflow template '%s' has not any task." % template.code)
                return False
            self.workflow = Workflow(scenario=self.scenario_id,
                                     code=template.code,
                                     template=template,
                                     priority=self.workflowpriority)
            self.workflow.save()
            self.log.debug("Created workflow '%s' for scenario '%s'." % (
                    template.code, self.scenario_id))
            self.bulk_tasks = []
            for template_task in template_tasks:
                task = WorkflowTask(workflow=self.workflow,
                                    code=template_task.code,
                                    parent_code=template_task.parent_code,
                                    max_failures=template_task.max_failures,
                                    max_duration_minutes=template_task.max_duration_minutes)
                task.save()
                self.bulk_tasks.append(task)
            self.log.debug("Created '%s' tasks for workflow '%s', scenario '%s'." % (
                    len(self.bulk_tasks), template.code, self.scenario_id))
            return True
        except Exception as ex:
            self.log.error("{0}".format(ex))
            return False


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
            instruction[task.code.name] = task.parent_code.name
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
        option["status"] = ""
        return option

    def start_workflow(self):
        """Sends trigger and logging messages to broker."""
        self.log.info("Start workflow")

        queues = self.root_queues()
        for queue in queues:
            self.set_current_task(queue)
            self.send_trigger_message(self.body,
                                 "Message emitted to queue %s" % queue,
                                 queue)

    def set_message_properties(self, priority=0, message_id=0):
        if self.workflow is not None:
            priority = self.workflow.priority
            message_id = self.workflow.id

        self.properties = BasicProperties(content_type="application/json",
                                          delivery_mode=2,
                                          priority=priority,
                                          message_id=str(message_id),
                                          timestamp=time.time())
