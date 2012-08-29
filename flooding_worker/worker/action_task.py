#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import simplejson
import platform
import time

from flooding_worker.worker.action import Action
from flooding_worker.perform_task import perform_task
from flooding_worker.worker.messaging_body import Body

import logging


class ActionTask(Action):

    def __init__(self, task_code, worker_nr):
        self.task_code = task_code
        self.worker_nr = worker_nr
        self.node = platform.node()
        # TODO set the logger properly on start worker
        self.log = logging.getLogger('flooding.action.task')
        super(ActionTask, self).__init__()

    def callback(self, ch, method, properties, body):
        """
        Sets channel as class variable.
        Runs a task.
        Sends message to next queue, back to the same queue or
        to queue with failed tasks depended on task result.
        """
        result_status = None
        self.channel = ch
        self.body = simplejson.loads(body)
        self.body[Body.WORKER_NR] = self.worker_nr
        self.body[Body.NODE] = self.node
        self.properties = properties

        if self.body.get(Body.IS_HEARTBEAT):
            self.body[Body.TIME] = time.time()
            self.body[Body.WORKER_STATUS] = Action.ALIVE
            self.log.info("HEARTBEAT")
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            return

        self.set_task_status(self.STARTED)
        self.log.info("Task is {}".format(self.STARTED))
        self.set_task_status("")

        try:
            result_status = perform_task(self.body["scenario_id"],
                                      int(self.task_code),
                                      self.worker_nr,
                                      self.broker_logging_handler)
        except Exception as ex:
            self.log.error("{0}".format(ex))
            result_status = False

        if self.status_task(result_status):
            self.set_task_status(self.SUCCESS)
            self.log.info(
                "Task is finished with {}.".format(self.SUCCESS))
            self.set_task_status("")
            self.proceed_next_trigger()
            self.log.info(
                "Task is {}.".format(self.QUEUED))
        else:
            self.set_task_status(self.FAILED)
            self.log.info("Task is {}".format(self.FAILED))
            self.set_task_status("")
            self.requeue_failed_message(ch, method)
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    def status_task(self, status=None):
        """
        Returns boolean.
        """
        if not status:
            return False
        if type(status).__name__ == 'boolean':
            return status
        if type(status).__name__ == 'tuple' and len(status) > 0:
            return status[0]
        return False

    def proceed_next_trigger(self):
        """
        Sends triggers to next queue(s).
        """
        queues = self.next_queues()
        for queue in queues:
            self.set_current_task(queue)
            self.send_trigger_message(self.body,
                                 "Message emitted to queue %s" % queue,
                                 queue)

    def decrease_failures(self):
        try:
            failures = int(self.body["max_failures_tmp"][self.task_code])
            self.body["max_failures_tmp"][self.task_code] = failures - 1
        except Exception as ex:
            self.log.error("{0}".format(ex))

    def requeue_failed_message(self, ch, method):
        """
        Sends message back to the origin queue or
        to the failed queue.
        """
        self.decrease_failures()
        if int(self.body["max_failures_tmp"][self.task_code]) >= 0:
            ch.basic_publish(exchange=method.exchange,
                             routing_key=method.routing_key,
                             body=simplejson.dumps(self.body),
                             properties=self.properties)
            self.log.info("Task requeued due failure.")
        else:
            self.body["max_failures_tmp"][self.task_code] = self.body[
                "max_failures"][self.task_code]
            ch.basic_publish(exchange="router",
                             routing_key="failed",
                             body=simplejson.dumps(self.body),
                             properties=self.properties)
            self.log.info("Task moved to failed queue due failure.")
