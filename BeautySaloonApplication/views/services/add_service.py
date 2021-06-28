from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from BeautySaloonApplication.forms import ServiceModelForm
from django.contrib.auth.decorators import login_required

# обрабатывает запрос на получение формы для заполнения
@login_required(redirect_field_name=None)
def add_service_form(request: HttpRequest):
    # добавлять услуги может только администратор
    if not request.user.is_staff:
        return HttpResponse(status=403)
    service_form = ServiceModelForm()
    page_html = render_to_string('creation/add_service_form.html', context={'service_form': service_form}, request=request)
    return HttpResponse(content=page_html)

# обрабатывает запрос на добавление услуги на основе заполненной ранее формы
@login_required(redirect_field_name=None)
def handle_service_form(request: HttpRequest):
    # добавлять услуги может только администратор
    if not request.user.is_staff:
        return HttpResponse(status=403)
    # сопоставим поля формы и с полями объекта ServiceModelForm
    service_form = ServiceModelForm(request.POST)
    response = HttpResponse(status=400)
    # сохраним новую услугу, если все поля корректны
    if service_form.is_valid():
        service_form.save()
        response = HttpResponseRedirect(redirect_to='/')
    return response
