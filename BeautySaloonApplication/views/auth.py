from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


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

    if session_user:
        login(request, session_user)
    else:
        if len(User.objects.filter(username=phone_number)) > 0:
            if is_registration:
                reason_description = "Номер телефона уже занят"
            else:
                reason_description = "Неправильный пароль или номер телефона уже занят"
            page_html = render_to_string('registration/login.html', context={
                'errors': True,
                'reason': {
                    'description': reason_description
                }
            })
            return HttpResponse(content=page_html, status=401)
        else:
            User.objects.create_user(username=phone_number, password=password)
    return HttpResponseRedirect(redirect_to='/')
