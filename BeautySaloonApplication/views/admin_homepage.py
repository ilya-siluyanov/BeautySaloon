from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string


@login_required(redirect_field_name=None)
def admin_homepage(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponseRedirect(redirect_to='/login', status=403)
    return HttpResponse(render_to_string('homepage.html'))
