from lizard_flooding_worker.models import Customer
from lizard_flooding_worker.models import Scenario
from lizard_flooding_worker.models import Logging
from lizard_flooding_worker.models import Task
from lizard_flooding_worker import models

from django.contrib import admin


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 0


class ScenarioInline(admin.TabularInline):
    model = Scenario
    extra = 0
    inlines = [Task]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class LoggingInline(admin.TabularInline):
    model = Logging
    extra = 0


class ScenarioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['customer', 'code']})
    ]
    inlines = [TaskInline]


class WorkerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name']})
    ]
    inlines = [ScenarioInline]


class LoggingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['customer', 'code']})
    ]
    inlines = [LoggingInline]


admin.site.register(Customer, WorkerAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Task)
#admin.site.register(Scenario, LoggingAdmin)
