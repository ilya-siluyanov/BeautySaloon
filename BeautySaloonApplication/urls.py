from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.client_homepage),
    path('login', views.logginer),
    path('logout', views.loggouter),
    path('signup', views.signuper),
    path('authorize', views.authorizer),
    path('register', views.registrator),
    path('make_order/<int:service_id>', views.send_order_form),
    path('cancel_order/<int:service_id>', views.cancel_order),
    path('send_order_form', views.handle_order_form),
    path('add_service', views.add_service_form),
    path('send_service_form', views.handle_service_form),
]
