from django.contrib import admin
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),  # URL for the login page
    path('dashboard/', views.dashboard, name="dashboard"),  # URL for the dashboard page
    path('create_post/', views.create_post, name="create_post"),  # URL for the dashboard page
    path('blogs_list/', views.blogs_list, name="blogs_list"),  
    path('blogs_details/', views.blogs_details, name="blogs_details"), 
    path('post_draft/<int:post_id>/', views.post_draft, name='post_draft'),
    path('draft_post/<int:post_id>/', views.draft_post, name='draft_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
