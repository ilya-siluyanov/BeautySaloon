from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from BeautySaloonApplication.models import Service


def client_homepage(request: HttpRequest):
    context = {
        'available_services': Service.objects.all()
    }
    return HttpResponse(content=render_to_string('client_homepage.html', context=context))
