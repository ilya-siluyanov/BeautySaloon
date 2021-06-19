from .homepage import client_homepage
from BeautySaloonApplication.views.orders.make_order import send_order_form, handle_order_form
from BeautySaloonApplication.views.services.add_service import add_service_form, handle_service_form
from .auth import logginer, loggouter, authorizer, registrator, signuper
from BeautySaloonApplication.views.orders.cancel_order import cancel_order
from BeautySaloonApplication.views.services.delete_service import delete_service
from BeautySaloonApplication.views.services.show_orders import show_orders
