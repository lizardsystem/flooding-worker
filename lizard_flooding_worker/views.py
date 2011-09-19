# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_flooding_worker.models import Customer
from lizard_flooding_worker.models import Scenario
from lizard_flooding_worker.models import Task
from lizard_flooding_worker.models import Logging

def homepage(request,
             customer_id=None,
             scenario_id=None,
             template="home.html"):
    """
    Main page for Mapdemo.
    """
    #customer_id = 1
    customers = Customer.objects.all()
    if customer_id is not None:
        scenarios = Scenario.objects.filter(customer=int(customer_id))
    else:
        scenarios = []
    if scenario_id is not None:
        loggings = Logging.objects.filter(scenario=int(scenario_id)).order_by('-time')
    else:
        loggings = Logging.objects.all().order_by('-time')
    return render_to_response(
        template,
        {"customers": customers,
         "scenarios": scenarios,
         "loggings": loggings},
        context_instance=RequestContext(request))
