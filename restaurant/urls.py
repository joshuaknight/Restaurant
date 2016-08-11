from django.conf.urls import url,include
from django.contrib import admin
from .views import * 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache

urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^user/$',user_view.as_view(),name = 'user_view'),
    url(r'^user/edit$',edit_view,name = 'edit_view'),
    url(r'^$', home.as_view(),name = 'home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/logout/$',never_cache(logout_),name = 'logout'),
    url(r'^accounts/login/$',never_cache(Login.as_view()),name = 'login'),
    url(r'^accounts/register/$', never_cache(signup.as_view()),name = 'register'),
    url(r'^contact/successful/$',contact_send,name='contact_send'),
    url(r'^recepie/$', login_required(add_recepie.as_view()),name = 'recepie'),
    url(r'^recepie/list$',render_recepie, name='render_recepie'),
    url(r'^recepie/list/recepie_search$',recepie_search, name='recepie_search'),
    url(r'^contact/$', contact.as_view(),name = 'contact'),
    url(r'^Book/table$', Order_Table.as_view(),name = 'table'),
    url(r'^Book/table/list$',render_table, name='render_table'),
    url(r'^Book/table/list/book_search$',book_search, name='search'),
    url(r'^order/$', Form.as_view(),name = 'order'),
    url(r'^order/mode/$',login_required(mode_of_pay.as_view()),name = 'mode_of_pay'),
    url(r'^order/mode/pay$', Order_Pay.as_view(),name = 'payement'),
    url(r'^order/mode/pay/internet/$',internet.as_view(),name = 'internet'),
    url(r'^order/current/$',render_order, name='current'),
    url(r'^order/current/delete$',delete, name='delete'),
    url(r'^social/', include("social.apps.django_app.urls",namespace="social")),     
    url(r'^about/$', about.as_view(),name = 'about'),

]
