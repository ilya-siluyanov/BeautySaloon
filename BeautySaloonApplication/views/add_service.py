from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from BeautySaloonApplication.forms import ServiceModelForm


def add_service_form(request: HttpRequest):
    service_form = ServiceModelForm()
    page_html = render_to_string('add_service_form.html', context={'service_form': service_form}, request=request)
    return HttpResponse(content=page_html)


def handle_service_form(request: HttpRequest):
    service_form = ServiceModelForm(request.POST)
    response = HttpResponse(content='хуйня твой инпут, заново делай', status=400)
    if service_form.is_valid():
        service_form.save()
        response = HttpResponseRedirect(redirect_to='/')
    return response
