from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect


@login_required(redirect_field_name=None)
def loggouter(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(redirect_to='/')
