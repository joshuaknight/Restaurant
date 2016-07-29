from django.conf.urls import url
from django.contrib import admin
from .views import * 
from contact.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home.as_view(),name = 'home'),
    url(r'^order/$', Form.as_view(),name = 'order'),
    url(r'^contact/$', contact.as_view(),name = 'contact'),
    url(r'^order/mode/$', mode_of_pay.as_view(),name = 'mode_of_pay'),
    url(r'^order/mode/pay$', Order_Pay.as_view(),name = 'payement'),
]
