from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string


@staff_member_required(redirect_field_name=None)
def admin_homepage(request: HttpRequest):
    return HttpResponse(render_to_string('admin_homepage.html'))
