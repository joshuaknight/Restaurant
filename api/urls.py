from django.conf.urls import url,include
from django.contrib import admin
from .views import * 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators import csrf 
from rest_framework.urlpatterns import format_suffix_patterns
from .serializers import * 
from django.views.decorators.csrf import csrf_protect


urlpatterns = [ 
    url(r'^comment/get$', get_comment.as_view(),name = 'list'),
    url(r'^schema$',schema_view,name = 'schema'),
    url(r'^comment/create$', create_comment.as_view(),name = 'create'),
    url(r'^comment/(?P<pk>\d+)/detail$', detail_comment.as_view(),name = 'detail'),
    url(r'^comment/(?P<pk>\d+)/update$', update_comment.as_view(),name = 'update'),
    url(r'^comment/(?P<pk>\d+)/delete$', delete_comment.as_view(),name = 'delete'),
]

#urlpatterns += format_suffix_patterns