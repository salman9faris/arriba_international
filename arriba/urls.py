
from django.contrib import admin
from django.urls import path,include

from django.conf import settings # to import static in deployment
from django.conf.urls.static import static # to import static in deployment

urlpatterns = [
    path("", include("dashboard.urls")),
    path("", include("home.urls")),
    path("api", include("api.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns = [


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
