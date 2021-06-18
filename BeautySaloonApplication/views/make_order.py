from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from BeautySaloonApplication import models, forms
from BeautySaloonApplication.models import Order, Client, Service
from django.contrib.auth.decorators import login_required


@api_view(['get'])
def send_order_form(request: HttpRequest, service_id: int):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/login')

    if len(Service.objects.filter(service_id=service_id)) == 0:
        return HttpResponseRedirect(redirect_to='/', status=404)
    form_initial_values = {
        'service_id': service_id,
        'phone_number': request.user.username
    }
    order_form = forms.OrderForm(initial=form_initial_values,
                                 auto_id=False)
    page_html = render_to_string('make_order_form.html',
                                 context={'order_form': order_form},
                                 request=request)
    return HttpResponse(page_html)


@api_view(['post'])
@login_required(redirect_field_name=None)
def handle_order_form(request: HttpRequest):
    received_order_form = forms.OrderForm(request.POST)
    response = None  # type: HttpResponse
    service_id = int(received_order_form.data['service_id'])

    if received_order_form.is_valid() and len(Service.objects.filter(service_id=service_id)):
        client = Client.objects.get(phone_number=request.user.username)
        service = Service.objects.get(service_id=service_id)
        received_order = received_order_form.cleaned_data
        received_order['date'] = eval(received_order['date'])
        new_order = Order.objects.create(client=client,
                                         service=service,
                                         date=received_order['date'][0],
                                         time=received_order['date'][1])
        new_order.save()
        response = HttpResponseRedirect(redirect_to='/')
    else:
        context = {
            'order_form': received_order_form,
            'errors': True,
            'reason': {
                'description': 'Проверьте данные ввода'
            }
        }
        html_text = render_to_string('make_order_form.html', context=context, request=request)
        response = HttpResponse(content=html_text, status=400)
    return response
