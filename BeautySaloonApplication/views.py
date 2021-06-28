from django.http import HttpRequest


def contact_page(request: HttpRequest):
    return HttpResponse(content=render_to_string('presentation/contact_page.html'))


from django.contrib.auth.decorators import login_required
from django.http import HttpRequest


@login_required(redirect_field_name=None)
def client_homepage(request: HttpRequest):
    context = {
        'available_services': [],
    }
    for service_instance in Service.objects.all():
        orders = Order.objects.filter(client_id=request.user.username).filter(service_id=service_instance)
        dict_to_context = {
            'service': service_instance
        }
        if len(orders) > 0:
            order = orders[0]
            dict_to_context['ordered'] = True
            dict_to_context['date'] = order.date
            dict_to_context['time'] = order.time
        context['available_services'].append(dict_to_context)
    return HttpResponse(content=render_to_string('presentation/homepage.html', context=context, request=request))


from django.http import HttpRequest
from BeautySaloonApplication.forms import ServiceModelForm
from django.contrib.auth.decorators import login_required


# обрабатывает запрос на получение формы для заполнения
@login_required(redirect_field_name=None)
def add_service_form(request: HttpRequest):
    # добавлять услуги может только администратор
    if not request.user.is_staff:
        return HttpResponse(status=403)
    service_form = ServiceModelForm()
    page_html = render_to_string('creation/add_service_form.html', context={'service_form': service_form},
                                 request=request)
    return HttpResponse(content=page_html)


# обрабатывает запрос на добавление услуги на основе заполненной ранее формы
@login_required(redirect_field_name=None)
def handle_service_form(request: HttpRequest):
    # добавлять услуги может только администратор
    if not request.user.is_staff:
        return HttpResponse(status=403)
    # сопоставим поля формы и с полями объекта ServiceModelForm
    service_form = ServiceModelForm(request.POST)
    response = HttpResponse(status=400)
    # сохраним новую услугу, если все поля корректны
    if service_form.is_valid():
        service_form.save()
        response = HttpResponseRedirect(redirect_to='/')
    return response


from django.http import HttpRequest
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


from typing import List

from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


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


from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from rest_framework.decorators import api_view


@api_view(['post'])
@login_required(redirect_field_name=None)
def cancel_order(request: HttpRequest, service_id: int):
    try:
        order = Order.objects.filter(client_id=request.user.username).get(service_id=service_id)
        order.delete()
    except Order.DoesNotExist:
        return HttpResponseRedirect(redirect_to='/', status=404)
    return HttpResponseRedirect(redirect_to='/')


from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from rest_framework.decorators import api_view

from BeautySaloonApplication import forms
from BeautySaloonApplication.models import Order, Service


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
    order_form = forms.OrderForm(initial=form_initial_values)
    page_html = render_to_string('creation/make_order_form.html',
                                 context={'order_form': order_form},
                                 request=request)
    return HttpResponse(page_html)


@api_view(['post'])
@login_required(redirect_field_name=None)
def handle_order_form(request: HttpRequest):
    received_order_form = forms.OrderForm(request.POST)
    service_id = int(received_order_form.data['service_id'])

    if received_order_form.is_valid() and len(Service.objects.filter(service_id=service_id)):
        client = Client.objects.get(phone_number=request.user.username)
        service = Service.objects.get(service_id=service_id)
        received_order = received_order_form.cleaned_data
        new_order = Order.objects.create(client=client,
                                         service=service,
                                         date=received_order['date'],
                                         time=received_order['time'])
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
        html_text = render_to_string('creation/make_order_form.html', context=context, request=request)
        response = HttpResponse(content=html_text, status=400)
    return response


from django.contrib.auth import authenticate
from django.http import HttpRequest
from rest_framework.decorators import api_view


@api_view(['POST'])
def authorizer(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')

    phone_number = request.POST['phone_number']
    password = request.POST['password']
    session_user = authenticate(username=phone_number, password=password)  # type: User
    context = {
        'errors': False,
        'reason': {
            'description': None
        }
    }
    if session_user:
        login(request, session_user)
    else:
        context['reason']['description'] = "Неправильный логин или пароль"

    if context['reason']['description']:
        context['errors'] = True
    if context['errors']:
        page_html = render_to_string('registration/login.html',
                                     request=request,
                                     context=context)
        return HttpResponse(content=page_html, status=401)
    return HttpResponseRedirect(redirect_to='/')


from django.http import HttpRequest


def logginer(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/login.html', request=request))


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest


@login_required(redirect_field_name=None)
def loggouter(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(redirect_to='/')


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
from rest_framework.decorators import api_view
from BeautySaloonApplication.models import Client


@api_view(['POST'])
def registrator(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    phone_number = request.POST.get('phone_number', None)
    name = request.POST.get('name', None)
    password = request.POST.get('password', None)
    is_staff = request.POST.get('is_staff_checkbox', None)
    if is_staff and is_staff == 'on':
        is_staff = True
    else:
        is_staff = False

    context = {
        'errors': False,
        'reason': {
            'description': None
        }
    }
    for field in (phone_number, name, password):
        if not field:
            context['reason']['description'] = "Ошибка регистрации. Проверьте данные и попробуйте ещё раз."

    first_condition = len(User.objects.filter(username=phone_number)) == 0
    second_condition = len(Client.objects.filter(phone_number=phone_number)) == 0 or is_staff
    allowed_to_register = first_condition and second_condition
    if allowed_to_register:
        with transaction.atomic():
            new_user = User.objects.create_user(username=phone_number, password=password, first_name=name)
            if is_staff:
                new_user.is_staff = is_staff
            new_user.save()
            if not is_staff:
                Client.objects.create(phone_number=new_user.username,
                                      name=name
                                      )
            login(user=new_user, request=request)
    else:
        context['reason']['description'] = "Номер телефона уже занят"
    if context['reason']['description']:
        context['errors'] = True
        return HttpResponse(
            render_to_string('registration/registration.html',
                             request=request,
                             context=context),
            status=400)
    else:
        return HttpResponseRedirect(redirect_to='/login')


from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template.loader import render_to_string


def signuper(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/registration.html', request=request))
