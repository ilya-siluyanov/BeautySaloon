from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template.loader import render_to_string


def signuper(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/registration.html', request=request))

