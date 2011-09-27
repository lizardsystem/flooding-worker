# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_flooding_worker.models import Workflow
from lizard_flooding.models import Task
from lizard_flooding_worker.models import Logging

def homepage(request,
             customer_id=None,
             workflow_id=None,
             template="home.html"):

    loggings = Logging.objects.all().order_by('-time')
    return render_to_response(
        template,
        {"customers": customers,
         "workflows": workflow,
         "loggings": loggings},
        context_instance=RequestContext(request))
