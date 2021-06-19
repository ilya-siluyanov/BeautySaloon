from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string


def logginer(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/')
    else:
        return HttpResponse(render_to_string('registration/login.html', request=request))
