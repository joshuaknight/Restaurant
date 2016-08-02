from django.conf.urls import url
from django.contrib import admin
from .views import * 
from django.contrib.auth.decorators import login_required 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home.as_view(),name = 'home'),
    url(r'^about/$', about.as_view(),name = 'about'),
    url(r'^contact/successful/$',(contact_send.as_view()),name='contact_send'),
    url(r'^recepie/$', add_recepie.as_view(),name = 'recepie'),
    url(r'^order/$', Form.as_view(),name = 'order'),
    url(r'^contact/$', contact.as_view(),name = 'contact'),
    url(r'^Book/table$', Order_Table.as_view(),name = 'table'),
    url(r'^order/mode/$', mode_of_pay.as_view(),name = 'mode_of_pay'),
    url(r'^order/mode/pay$', Order_Pay.as_view(),name = 'payement'),
    url(r'^recepie/list$',render_recepie, name='render_recepie'),
    url(r'^Book/table/list$',render_table, name='render_table'),
]
