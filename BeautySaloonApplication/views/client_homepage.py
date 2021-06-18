from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from BeautySaloonApplication.models import Service
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None)
def client_homepage(request: HttpRequest):
    context = {
        'available_services': Service.objects.all()
    }
    return HttpResponse(content=render_to_string('client_homepage.html', context=context))
