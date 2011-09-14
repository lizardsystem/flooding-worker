#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

import sys
import time
import logging
from datetime import datetime
import simplejson
from pika import BlockingConnection
from pika import BasicProperties
from pika import ConnectionParameters
from pika import PlainCredentials

from brokerconfig import CONNECT_SETTINGS
from brokerconfig import QUEUES

from lizard_flooding_worker.models import Customer
from lizard_flooding_worker.models import Scenario
from lizard_flooding_worker.models import Task
from lizard_flooding_worker.models import Logging

import tmp_jbo
from message_logging_handler import AMQPMessageHandler


def retrieve_scenario_options(scenario_id):
        """Retrieves scenario info from database.
        1 task_code per scenario
        for example:
        wel (120, 130, (160, 132))
        not (120, 120, 130, (160, 132))"""

        tasks = Task.objects.all().filter(scenario=scenario_id)
        scenario = Scenario.objects.get(pk=scenario_id)
        option = {}
        instruction = {}
        for task in tasks:
                if int(task.sequence) == 1:
                        option["curr_task_code"] = task.code
                instruction[task.code] = task.sequence
        option["instruction"] = instruction
        option["customer_id"] = scenario.customer.id
        option["scenario_id"] = scenario_id
        option["priority"] = ""
        option["curr_log_level"] = ""
        option["message"] = ""
        option["event_time"] = ""
        option["next_sequence"] = 1
        return option

def retrieve_queue_options(queue_code):
        """Retrieves queue info from brokerconfig file."""
        return QUEUES[queue_code]

def connect_to_broker():
        credentials = PlainCredentials(CONNECT_SETTINGS["BROKER_USER"],
                                       CONNECT_SETTINGS["BROKER_PASSWORD"])
        parameters = ConnectionParameters(host = CONNECT_SETTINGS["BROKER_HOST"],
                                          port = CONNECT_SETTINGS["BROKER_PORT"],
                                          virtual_host = CONNECT_SETTINGS["BROKER_VHOST"],
                                          credentials = credentials)
        connection = BlockingConnection(parameters)
        return connection

def create_logging_body(body, message, log_level="0"):
        """Create a new body dict"""
        if (type(body).__name__ == "str"):
                options = simplejson.loads(body)
        else:
                 options = body.copy()
        options["message"] = message
        options["curr_log_level"] = log_level
        options["event_time"] = time.time()
        return options

def publish_message(channel, queue_options, body, properties=None):
        """Sends a message to broker. """
        properties = BasicProperties(content_type = "application/json",
                                     delivery_mode = 2)
        channel.basic_publish(exchange=queue_options["exchange"],
                              routing_key=queue_options["binding_key"],
                              body=simplejson.dumps(body),
                              properties=properties)

def start_scenario(scenario_id, queue_code):
        """Sends a start and logging message to broker."""
        connection = connect_to_broker()
        channel = connection.channel()
        task_options = retrieve_scenario_options(scenario_id)
        task_queue_options = retrieve_queue_options(queue_code)
        logging_queue_options = retrieve_queue_options("logging")
        # send logging
        logging_body = create_logging_body("Start scenario", task_options)
        publish_message(channel, logging_queue_options, logging_body)
        # send trigger
        publish_message(channel, task_queue_options, task_options)
        # send logging
        logging_body = create_logging_body("Started scenario", task_options)
        publish_message(channel, logging_queue_options, logging_body)
        connection.close()

def send_logging_message(body, message, log_level="0"):
        connection = connect_to_broker()
        channel = connection.channel()
        logging_body = create_logging_body(body, message, log_level)
        queue_options = retrieve_queue_options("logging")
        publish_message(channel, queue_options, logging_body)
        connection.close()

def send_trigger_message(body, message, queue):
        connection = connect_to_broker()
        channel = connection.channel()
        queue_options = retrieve_queue_options(queue)
        publish_message(channel, queue_options, body)
        connection.close()

def do_some_job(body):
        """Sleeps 15 seconds."""

        logger = logging.getLogger("Worker Number")
        logging.handlers.AMQPMessageHandler = AMQPMessageHandler
        amqp_handler = logging.handlers.AMQPMessageHandler(body)
        amqp_handler.setLevel(logging.DEBUG)
        logger.addHandler(amqp_handler)
        print "Run the job."
        tmp_job.main(logger, body)
        print "I'm going to sleep 15 seconds."
        time.sleep(15)
        print "I'm back."

def next_queues(body):
        next_sequence = int(body["next_sequence"]) + 1
        instruction = body["instruction"]
        queues = []
        for (queue_code,sequence) in instruction.iteritems():
                if int(sequence) == next_sequence:
                        queues.append(queue_code)
        return queues

def increase_sequence(body):
        body["next_sequence"] = int(body["next_sequence"]) + 1

def set_current_task(body, queue):
        body["curr_task_code"] = queue

def callback(ch, method, properties, body):
        #sends logging to logging queue
        #raise Exception("I know python!")
        body_dict = simplejson.loads(body)
        send_logging_message(body_dict, "Start task")
        do_some_job(body)
        send_logging_message(body_dict, "End task")
        queues = next_queues(body_dict)
        increase_sequence(body_dict)
        for queue in queues:
                set_current_task(body_dict, queue)
                send_trigger_message(body_dict,
                                     "Message emitted to queue %s" % queue,
                                     queue)
        ch.basic_ack(delivery_tag = method.delivery_tag)

def callback_logging(ch, method, properties, body):
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
                ch.basic_ack(delivery_tag = method.delivery_tag)
        except Exception as ex:
                print ex

def run_worker(queue_code):
        """Runs common worker. """

        connection = connect_to_broker()
        channel = connection.channel()
        channel.basic_consume(callback,
                              queue=queue_code,
                              no_ack=False)
        channel.start_consuming()

def run_logging_worker(queue_code):
        """Runs logging worker."""
        connection = connect_to_broker()
        channel = connection.channel()
        channel.basic_consume(callback_logging,
                              queue=queue_code,
                              no_ack=False)
        channel.start_consuming()
