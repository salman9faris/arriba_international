
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("", include("dashboard.urls")),
    path("", include("home.urls")),
    path("api", include("api.urls")),
    path('admin/', admin.site.urls),
]

