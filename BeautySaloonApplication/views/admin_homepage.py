from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string


@login_required(redirect_field_name=None)
def admin_homepage(request: HttpRequest):
    return HttpResponse(render_to_string('admin_homepage.html'))
