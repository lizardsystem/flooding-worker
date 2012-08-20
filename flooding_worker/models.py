# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import logging
from django.db import models
from flooding_worker.worker.action import Action

LOGGING_LEVELS = (
    (0, u'DEBUG'),
    (1, u'INFO'),
    (2, u'WARNING'),
    (3, u'ERROR'),
    (4, u'CRITICAL'),
)


STATUSES = (
    (Action.QUEUED, Action.QUEUED),
    (Action.STARTED, Action.STARTED),
    (Action.SUCCESS, Action.SUCCESS),
    (Action.FAILED, Action.FAILED),
)


logger = logging.getLogger(__name__)


class WorkflowTemplate(models.Model):
    DEFAULT_TEMPLATE_CODE = 1
    IMPORTED_TEMPLATE_CODE = 2

    code = models.IntegerField(max_length=30)

    def __unicode__(self):
        return str(self.code)

    class Meta:
        db_table = 'flooding_worker_workflowtemplate'


class Workflow(models.Model):

    code = models.CharField(max_length=100)
    template = models.ForeignKey(WorkflowTemplate, blank=True, null=True)
    scenario = models.IntegerField(blank=True, null=True)
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

    def get_status(self):
        tasks = self.w.workflowtask_set.all()
        for task in tasks:
            if task.status == 0:
                return task.status

    def is_success(self):
        tasks = self.workflowtask_set.all()
        success_tasks = self.workflowtask_set.filter(status=Action.SUCCESS)
        return (len(tasks) == len(success_tasks))

    def is_queued(self):
        tasks = self.workflowtask_set.all()
        none_status_tasks = self.workflowtask_set.filter(status=None)
        queued_status_tasks = self.workflowtask_set.filter(
            status=Action.QUEUED)
        return (
            len(none_status_tasks) + len(queued_status_tasks) == len(tasks))

    def is_failed(self):
        statuses = self.workflowtask_set.values_list(
            'status', flat=True)
        return (Action.FAILED in statuses)

    def __unicode__(self):
        return self.code

    class Meta:
        db_table = 'flooding_worker_workflow'


class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'flooding_worker_tasktype'
        ordering = ('name',)


class WorkflowTemplateTask(models.Model):
    code = models.ForeignKey(TaskType)
    parent_code = models.ForeignKey(
        TaskType, null=True, related_name='parent_task_code',
        help_text="Define a task's tree, None = end of the tree.")
    max_failures = models.IntegerField(default=0)
    max_duration_minutes = models.IntegerField(default=0)
    workflow_template = models.ForeignKey(WorkflowTemplate)

    def __unicode__(self):
        return self.code.name

    class Meta:
        db_table = 'flooding_worker_workflowtemplatetask'


class WorkflowTask(models.Model):
    workflow = models.ForeignKey(Workflow)
    code = models.ForeignKey(TaskType)
    parent_code = models.ForeignKey(
        TaskType, null=True, related_name='workflowtask_parent_task_code',
        help_text="Define a task's tree, None = end of the tree.")
    max_failures = models.IntegerField(default=0)
    max_duration_minutes = models.IntegerField(default=0)
    tstart = models.DateTimeField(blank=True, null=True)
    tfinished = models.DateTimeField(blank=True, null=True)
    successful = models.NullBooleanField(blank=True, null=True)
    status = models.CharField(choices=STATUSES,
                              blank=True, null=True,
                              max_length=25)

    def __unicode__(self):
        return self.code.name

    class Meta:
        db_table = 'flooding_worker_workflowtask'


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
        db_table = 'flooding_worker_logging'
