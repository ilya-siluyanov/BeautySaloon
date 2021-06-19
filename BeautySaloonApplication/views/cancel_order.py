from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from BeautySaloonApplication import models, forms
from BeautySaloonApplication.models import Order, Client, Service
from django.contrib.auth.decorators import login_required


@api_view(['post'])
@login_required(redirect_field_name=None)
def cancel_order(request: HttpRequest, service_id: int):
    try:
        order = Order.objects.filter(client_id=request.user.username).get(service_id=service_id)
        order.delete()
    except Order.DoesNotExist:
        return HttpResponseRedirect(redirect_to='/', status=404)
    return HttpResponseRedirect(redirect_to='/')
