from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from BeautySaloonApplication import models, forms
from BeautySaloonApplication.models import Order, Client, Service
from django.contrib.auth.decorators import login_required


@api_view(['get'])
def send_order_form(request: HttpRequest, service_id: int):
    session_user = request.user
    order_form = forms.OrderForm(initial={'service_id': service_id}, auto_id=False)
    page_html = render_to_string('make_order_form.html',
                                 context={'order_form': order_form},
                                 request=request)
    return HttpResponse(page_html)


@api_view(['post'])
@login_required(redirect_field_name=None)
def handle_order_form(request: HttpRequest):
    received_order_form = forms.OrderForm(request.POST)
    response = None  # type: HttpResponse
    service_id = received_order_form.data['service_id']
    if received_order_form.is_valid() and len(Service.objects.filter(service_id=service_id)):
        response = HttpResponseRedirect(redirect_to='/')
    else:
        context = {
            'order_form': received_order_form,
            'wrong_input': True
        }
        html_text = render_to_string('make_order_form.html', context=context)
        response = HttpResponse(content=html_text, status=400)
    return response
