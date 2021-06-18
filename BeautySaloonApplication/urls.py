from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.client_homepage),
    path('login', views.logginer),
    path('logout', views.loggouter),
    path('authorize', views.authorizer),
    path('make_order/<int:service_id>', views.send_order_form),
    path('send_order_form', views.handle_order_form),
    path('admin', views.admin_homepage),
    path('admin/add_service', views.add_service_form),
    path('admin/send_service_form', views.handle_service_form),
]
