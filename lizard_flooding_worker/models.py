# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from django.db import models
#from lizard_flooding.models import Scenario
#from lizard_flooding.models import TaskType

LOGGING_LEVELS = (
    (0, u'DEBUG'),
    (1, u'INFO'),
    (2, u'WARNING'),
    (3, u'ERROR'),
    (2, u'CRITICAL'),
)


logger = logging.getLogger(__name__)


class Workflow(models.Model):
    scenario = models.ForeignKey('flooding-lib.Scenario')
    code = models.CharField(max_length=100)
    tstart = models.DateTimeField(
        blank=True,
        null=True)
    tfinished = models.DateTimeField(
        blank=True,
        null=True)
    logging_level = models.IntegerField(
        choices=LOGGING_LEVELS,
        blank=True,
        null=True)
    priority = models.IntegerField(
        blank=True,
        null=True)

    def __unicode__(self):
        return self.code


class WorkflowTemplate(models.Model):
    code = models.IntegerField(max_length=30)

    def __unicode__(self):
        return str(self.code)


class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class WorkflowTemplateTask(models.Model):
    code = models.ForeignKey(TaskType)
    sequence = models.IntegerField()
    max_failures = models.IntegerField(default=0)
    max_duration_minutes = models.IntegerField(default=0)
    workflow_template = models.ForeignKey(WorkflowTemplate)

    def __unicode__(self):
        return self.code.name


class WorkflowTask(models.Model):
    workflow = models.ForeignKey(Workflow)
    code = models.ForeignKey(TaskType)
    sequence = models.IntegerField()
    max_failures = models.IntegerField(default=0)
    max_duration_minutes = models.IntegerField(default=0)
    tstart = models.DateTimeField(blank=True, null=True)
    tfinished = models.DateTimeField(blank=True, null=True)
    successful = models.NullBooleanField(blank = True, null=True)

    def __unicode__(self):
        return self.code.name


class Logging(models.Model):
    workflow = models.ForeignKey(Workflow)
    task = models.ForeignKey(WorkflowTask)
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

