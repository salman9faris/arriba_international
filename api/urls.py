

from django.contrib import admin
from django.urls import path,include
from home import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
      path("/alldoc",views.alldocapi,name='alldocapi'),  
      path("/doc/<pk>",views.docapi,name='docapi'),  
      path("/allagency",views.allagencyapi,name='allagencyapi'),
      path("/docbyagency/<pk>",views.docbyagencyapi,name='docbyagencyapi'),  
      path("/trackdoc/<pk>",views.trackingapi,name='trackingapi'),  
       path("/totaldoc",views.totaldoccount,name='totaldoccount'),  
       path("/refresh",views.refresh,name='refresh'),  
]