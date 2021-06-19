from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string


def contact_page(request: HttpRequest):
    return HttpResponse(content=render_to_string('presentation/contact_page.html'))
