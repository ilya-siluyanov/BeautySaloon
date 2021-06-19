from typing import List

from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from BeautySaloonApplication.models import Service, Order
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required(redirect_field_name=None)
def show_orders(request: HttpRequest, service_id: int):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    try:
        service = Service.objects.get(service_id=service_id)
    except Service.DoesNotExist:
        return HttpResponse(status=403)
    context = {
        'service': {
            'name': service.name,
            'price': service.price,
        },
        'orders': [],
    }
    orders = list(service.orders.all())  # type: List[Order]
    for order in orders:
        client = order.client
        context['orders'].append({
            'client_name': client.name,
            'client_date': order.date,
            'client_time': order.time,
            'client_phone_number': client.phone_number
        })
    html_page = render_to_string('presentation/show_orders.html', request=request, context=context)
    return HttpResponse(content=html_page)
