from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),  # URL for the login page
    path('dashboard/', views.dashboard, name="dashboard"),  # URL for the dashboard page
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
