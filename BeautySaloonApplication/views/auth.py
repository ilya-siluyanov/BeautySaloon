from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from BeautySaloonApplication.models import Client
from django.db import transaction


def logginer(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/login.html', request=request))


def signuper(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/registration.html', request=request))


@login_required(redirect_field_name=None)
def loggouter(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(redirect_to='/')


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

    if session_user.is_staff:
        return HttpResponseRedirect(redirect_to='/admin')
    else:
        return HttpResponseRedirect(redirect_to='/')


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
    for field in (phone_number, name, password, is_staff):
        if not field:
            context['reason']['description'] = "Ошибка регистрации. Проверьте данные и попробуйте ещё раз."

    first_condition = len(User.objects.filter(username=phone_number)) == 0
    second_condition = len(Client.objects.filter(phone_number=phone_number)) == 0 or is_staff
    allowed_to_register = first_condition and second_condition
    if allowed_to_register:
        with transaction.atomic():
            new_user = User.objects.create_user(username=phone_number, password=password)
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
        return HttpResponseRedirect(redirect_to='/login', status=200)
