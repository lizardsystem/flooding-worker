# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.shortcuts import render_to_response
from django.views.generic import View

from django.contrib.sites.models import get_current_site
from flooding_worker.models import Workflow, WorkflowTask
from flooding_worker.models import Logging
from flooding_worker import executor


class WorkflowTasksView(View):

    template = 'workflow_tasks.html'

    def get(self, request, workflow_id=None):
        context = {'tasks': self.tasks(workflow_id),
                   'workflow': self.get_workflow(workflow_id)}
        return render_to_response(self.template, context)

    def post(self, request, workflow_id=None):
        task_id = request.POST.get('task_id')
        task_code = request.POST.get('task_code')
        success = executor.start_task(task_id)
        msg = "Taak code {0} is {1} geplaatst in de wachtrij."
        if success:
            msg = msg.format(task_code, '')
        else:
            msg = msg.format(task_code, 'NIET')
        context = {'tasks': self.tasks(workflow_id),
                   'msg': msg,
                   'workflow': self.get_workflow(workflow_id)}
        return render_to_response(self.template, context)

    def get_workflow(self, workflow_id):
        if workflow_id is not None:
            return Workflow.objects.get(pk=workflow_id)

    def tasks(self, workflow_id):
        if workflow_id is None:
            return {}
        else:
            tasks = WorkflowTask.objects.filter(workflow__id=workflow_id)
            return tasks


class WorkflowsView(View):

    template = 'workflows.html'

    def get(self, request, scenario_id=None):
        workflows = Workflow.objects.filter(
            scenario=scenario_id).order_by('-tcreated')

        context = {'workflows': workflows,
                   'scenario_id': scenario_id,
                   'current_site': get_current_site(request)}
        return render_to_response(self.template, context)


class LoggingView(View):

    template = 'logging.html'

    def get(self, request, workflow_id=None, task_id=None, scenario_id=None):
        context = {'scenario_id': scenario_id,
                   'workflow_id': workflow_id,
                   'task_id': task_id}

        if task_id is not None:
            options = {'task__id': task_id}
        elif workflow_id is not None:
            options = {'workflow__id': workflow_id}
        else:
            options = {}

        loggings = Logging.objects.filter(**options).order_by('-time')

        context.update({'loggings': loggings})
        return render_to_response(self.template, context)
