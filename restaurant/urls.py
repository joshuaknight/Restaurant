from django.conf.urls import url,include
from django.contrib import admin
from .views import * 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators import csrf 
from django.contrib.auth.views import *


admin.site.index_template = 'admin.html'
admin.autodiscover()

urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^user/$',login_required(user_view.as_view()),name = 'user_view'),
    url(r'^user/edit$',edit_view,name = 'edit_view'),
    url(r'^$', home.as_view(),name = 'home'),
     #  url(r'^test/$',test.as_view(),name = 'test'),
    url(r'^admin/', admin.site.urls),
    
    # password reset urls imported from django auth.views 
    url(r'^user/password/reset/$',password_reset,
        {'post_reset_redirect' : '/user/password/reset/done/'},
                                    name="password_reset"),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, name='password_reset_confirm'),

    url(r'^user/password/reset/done/$',password_reset_done),    

    url(r'^user/password/done/$',
        password_reset_complete,name = 'password_reset_complete'),

    #oauth2
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

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

    url(r'^order/$', new_order.as_view(),name = 'order'),
    url(r'^order/add/(?P<pk>\d+)', add_order,name = 'add_order'),
    url(r'^order/create$', create_order.as_view(),name = 'create_order'),
    url(r'^order/current/$',render_order.as_view(), name='current'),
    url(r'^order/delete/(?P<pk>\d+)', order_delete.as_view(),name = 'order_delete'),
    
    url(r'^order/cart/$',cart.as_view(), name='cart'),
    url(r'^order/mode/$',login_required(mode_of_pay.as_view()),name = 'mode_of_pay'),
    url(r'^order/mode/pay$', Order_Pay.as_view(),name = 'payement'),
    url(r'^order/mode/pay/internet/$',internet.as_view(),name = 'internet'),    
    url(r'^social/', include("social.apps.django_app.urls",namespace="social")),     
    url(r'^about/$', about.as_view(),name = 'about'),
    url(r'^comment/$', comment.as_view(),name = 'comment'),
    url(r'^api/', include('api.urls'),name= 'comment-api'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

