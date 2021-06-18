from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string


def admin_homepage(request: HttpRequest):
    return HttpResponse(render_to_string('admin_homepage.html'))
