#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson
from datetime import datetime

from flooding_worker.worker.action import Action
from flooding_worker.models import WorkflowTask
from flooding_worker.models import Logging

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
        # TODO move keys of body to Action class as class variables
        task_code = body_dict.get("curr_task_code", None)
        # TODO Implement logging of root/supervisor worker
        if task_code is None:
            #ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        tasks = body_dict.get("workflow_tasks", None)
        event_time = body_dict.get("event_time")
        task_id = None
        if tasks is not None:
            task_id = tasks.get(task_code, None)
            print task_id
        task_status = body_dict.get("status", None)
        if task_status is not None and task_status != "":
            self.store_task_status(task_id, task_status, event_time)
        # TODO [:200]
        message = body_dict["message"][:200]
        try:
            new_logging = Logging(
                workflow_id=body_dict["workflow_id"],
                task=WorkflowTask(pk=task_id),
                time=datetime.today(),
                level=body_dict["curr_log_level"],
                message=message)
            new_logging.save()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            log.error(",".join(map(str, ex.args)))

    def retrieve_body(self):
        """ Return to insrt into db
        """

    def store_task_status(self, task_id, status, event_time):
        """
        Save status and event time to database
        
        Arguments:
        event_time - "", float or None
        """
        task = WorkflowTask.objects.get(pk=task_id)
        task.status = status
        if isinstance(event_time, datetime) or event_time == "":
            task.set_action_time()
        else:
            print type(event_time), status
            print event_time
            print "From timestamp", datetime.fromtimestamp(event_time)
            task.set_action_time(datetime.fromtimestamp(event_time))
            print "task event_time set {}.".format(task.tfinished)
        task.save()
        
