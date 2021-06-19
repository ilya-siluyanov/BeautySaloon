from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from rest_framework.decorators import api_view

from BeautySaloonApplication.models import Order


@api_view(['post'])
@login_required(redirect_field_name=None)
def cancel_order(request: HttpRequest, service_id: int):
    try:
        order = Order.objects.filter(client_id=request.user.username).get(service_id=service_id)
        order.delete()
    except Order.DoesNotExist:
        return HttpResponseRedirect(redirect_to='/', status=404)
    return HttpResponseRedirect(redirect_to='/')
