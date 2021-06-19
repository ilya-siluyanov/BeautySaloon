from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from BeautySaloonApplication.forms import ServiceModelForm
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name=None)
def add_service_form(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    service_form = ServiceModelForm()
    page_html = render_to_string('creation/add_service_form.html', context={'service_form': service_form}, request=request)
    return HttpResponse(content=page_html)


@login_required(redirect_field_name=None)
def handle_service_form(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    service_form = ServiceModelForm(request.POST)
    response = HttpResponse(content='хуйня твой инпут, заново делай', status=400)
    if service_form.is_valid():
        service_form.save()
        response = HttpResponseRedirect(redirect_to='/admin')
    return response
