# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_flooding_worker.models import Customer
from lizard_flooding_worker.models import Workflow
from lizard_flooding.models import Task
from lizard_flooding_worker.models import Logging

def homepage(request,
             customer_id=None,
             workflow_id=None,
             template="home.html"):
    """
    Main page for Mapdemo.
    """
    #customer_id = 1
    customers = Customer.objects.all()
    if customer_id is not None:
        workflow = Workflow.objects.filter(customer=int(customer_id))
    else:
        workflows = []
    if workflow_id is not None:
        loggings = Logging.objects.filter(workflow=int(workflow_id)).order_by('-time')
    else:
        loggings = Logging.objects.all().order_by('-time')
    return render_to_response(
        template,
        {"customers": customers,
         "workflows": workflow,
         "loggings": loggings},
        context_instance=RequestContext(request))
