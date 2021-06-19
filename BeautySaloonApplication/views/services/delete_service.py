from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.db import transaction
from BeautySaloonApplication.models import Service, Order
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None)
def delete_service(request: HttpRequest, service_id: int):
    if not request.user.is_staff:
        return HttpResponse(status=403)

    with transaction.atomic():
        try:
            service = Service.objects.get(service_id=service_id)
        except Service.DoesNotExist:
            return HttpResponse(status=404)
        orders = Order.objects.filter(service_id=service_id)
        for order in orders:
            order.delete()
        service.delete()
    return HttpResponseRedirect(redirect_to='/')
