from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from BeautySaloonApplication.models import Client


def logginer(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/login.html', request=request))


@login_required(redirect_field_name=None)
def loggouter(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(redirect_to='/')


def authorizer(request: HttpRequest):
    phone_number = request.POST['phone_number']
    password = request.POST['password']
    is_registration = True if request.POST['is_registration'] == '1' else False
    session_user = authenticate(username=phone_number, password=password)
    context = {
        'errors': False,
        'reason': {
            'description': None
        }
    }
    if is_registration:
        if len(User.objects.filter(username=phone_number)) == 0:
            new_user = User.objects.create_user(username=phone_number, password=password)
            Client.objects.create(phone_number=new_user.username,
                                  name='Name',  # FIXME
                                  surname='Surname')  # FIXME
            login(user=new_user, request=request)
        else:
            context['reason']['description'] = "Номер телефона уже занят"
    else:
        if len(Client.objects.filter(phone_number=phone_number)) > 0:
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
