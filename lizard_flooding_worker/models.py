# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from django.db import models
from lizard_flooding.models import Scenario


LOGGING_LEVELS = (
    (0, u'DEBUG'),
    (1, u'INFO'),
    (2, u'WARNING'),
    (3, u'ERROR'),
    (2, u'CRITICAL'),
)

PRIORITIES = (
    (0, u'low'),
    (1, u'high'),
)


logger = logging.getLogger(__name__)


class Customer(models.Model):
    name = models.CharField(max_length=30)
    actief = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Workflow(models.Model):
    customer = models.ForeignKey(Customer)
    scenario = models.ForeignKey(Scenario)
    code = models.CharField(max_length=100)
    start_time = models.DateTimeField(
        blank=True,
        null=True)
    end_time = models.DateTimeField(
        blank=True,
        null=True)
    logging_level = models.IntegerField(
        choices=LOGGING_LEVELS,
        blank=True,
        null=True)
    priority = models.IntegerField(
        choices=PRIORITIES,
        blank=True,
        null=True)

    def __unicode__(self):
        return self.code


class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class WorkflowTask(models.Model):
    workflow = models.ForeignKey(Workflow)
    code = models.ForeignKey(TaskType)
    scenario = models.ForeignKey(Scenario)
    sequence = models.IntegerField()
    tstart = models.DateTimeField(blank=True, null=True)
    tfinished = models.DateTimeField(blank=True, null=True)
    errorlog = models.TextField(blank=True, null=True)
    successful = models.NullBooleanField(blank = True, null=True)

    def __unicode__(self):
        return self.code


class Logging(models.Model):
    customer = models.ForeignKey(Customer)
    workflow = models.ForeignKey(Workflow)
    task = models.ForeignKey(WorkflowTask)
    scenario = models.ForeignKey(Scenario)
    time = models.DateTimeField(
        blank=True,
        null=True)
    level = models.IntegerField(
        choices=LOGGING_LEVELS,
        blank=True,
        null=True)
    message = models.CharField(max_length=200)

    class Meta:
        get_latest_by = "time"

