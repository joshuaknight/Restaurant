from django.conf.urls import url
from django.contrib import admin
from .views import * 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home.as_view(),name = 'home'),
    url(r'^order/$', Form.as_view(),name = 'order'),
    url(r'^order/pay$', Order_Pay.as_view(),name = 'payement'),
]
