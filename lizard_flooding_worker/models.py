# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from django.db import models


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

TASK_CODES = (
    ('120', "120"),
    ('130', "130"),
    ('132', "132"),
    ('160', "160"),
)

logger = logging.getLogger(__name__)


class Customer(models.Model):
    name = models.CharField(max_length=30)
    actief = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Scenario(models.Model):
    customer = models.ForeignKey(Customer)
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


class Task(models.Model):
    scenario = models.ForeignKey(Scenario)
    code = models.CharField(
        choices=TASK_CODES,
        max_length=4,
        blank=True,
        null=True)
    started_at = models.DateTimeField(
        blank=True,
        null=True)
    ended_at = models.DateTimeField(
        blank=True,
        null=True)
    sequence = models.IntegerField()

    def __unicode__(self):
        return self.code


class Logging(models.Model):
    customer = models.ForeignKey(Customer)
    scenario = models.ForeignKey(Scenario)
    task = models.ForeignKey(Task)
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

