from lizard_flooding_worker.models import Customer
from lizard_flooding_worker.models import Workflow
from lizard_flooding_worker.models import Logging
from lizard_flooding_worker.models import WorkflowTask
from lizard_flooding_worker.models import TaskType

from django.contrib import admin


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 0


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


class WorkflowAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['customer', 'code']})
    ]
    inlines = [TaskInline]


class WorkerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name']})
    ]
    inlines = [WorkflowInline]


class LoggingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['customer', 'code']})
    ]
    inlines = [LoggingInline]


admin.site.register(Customer, WorkerAdmin)
admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(WorkflowTask)
admin.site.register(TaskType)
#admin.site.register(Workflow, LoggingAdmin)
