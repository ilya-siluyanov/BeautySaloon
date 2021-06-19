from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string

from BeautySaloonApplication.models import Service, Order


@login_required(redirect_field_name=None)
def client_homepage(request: HttpRequest):
    context = {
        'available_services': [],
        'client': {
            'name': request.user.first_name,
            'is_staff': request.user.is_staff
        }
    }

    for service_instance in Service.objects.all():
        orders = Order.objects.filter(client_id=request.user.username).filter(service_id=service_instance)
        dict_to_context = {
            'service_instance': service_instance
        }
        if len(orders) > 0:
            order = orders[0]
            dict_to_context['ordered'] = True
            dict_to_context['date'] = order.date
            dict_to_context['time'] = order.time
        context['available_services'].append(dict_to_context)
    return HttpResponse(content=render_to_string('homepage.html', context=context, request=request))
