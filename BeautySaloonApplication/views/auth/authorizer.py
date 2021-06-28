from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
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
