from lizard_flooding_worker.models import Workflow
from lizard_flooding_worker.models import Logging
from lizard_flooding_worker.models import WorkflowTask
from lizard_flooding_worker.models import WorkflowTemplate
from lizard_flooding_worker.models import WorkflowTemplateTask
from lizard_flooding_worker.models import TaskType

from django.contrib import admin


class WorkflowInline(admin.TabularInline):
    model = Workflow
    extra = 0
    inlines = [WorkflowTask]


class TaskInline(admin.TabularInline):
    model = WorkflowTask
    extra = 0


class LoggingInline(admin.TabularInline):
    model = Logging
    extra = 0


class WorkflowTemplateTaskInline(admin.TabularInline):
    model = WorkflowTemplateTask
    extra = 0


class WorkflowAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['code', 'scenario']})
    ]
    inlines = [TaskInline]


class WorkerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name']})
    ]
    inlines = [WorkflowInline]


class WorkflowTemplateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['code']})
    ]
    inlines = [WorkflowTemplateTaskInline]


admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowTask)
admin.site.register(TaskType)
admin.site.register(WorkflowTemplate, WorkflowTemplateAdmin)
