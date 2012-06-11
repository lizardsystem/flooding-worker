#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson
from datetime import datetime

from flooding_worker.models import Workflow
from flooding_worker.models import WorkflowTask
from flooding_worker.models import TaskType
from flooding_worker.models import Logging

from flooding_worker.worker.action import Action

import logging
log = logging.getLogger('flooding.action_logging')


class ActionLogging(Action):

    def callback(self, ch, method, properties, body):
        """
        Inserts logging data into database.
        Used by logging_worker.
        Cuts message to max. 200 chars.
        """
        body_dict = simplejson.loads(body)
        task_code = body_dict["curr_task_code"]
        task_id = body_dict["workflow_tasks"][task_code]
        message = body_dict["message"][:200]
        try:
            new_logging = Logging(
                workflow_id=body_dict["workflow_id"],
                task = WorkflowTask(pk=task_id),
                time=datetime.utcfromtimestamp(body_dict["event_time"]),
                level=body_dict["curr_log_level"],
                message=message)
            new_logging.save()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            log.error("{0}".format(ex))
