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
    path('backtodashboard/', views.backtodashboard, name='backtodashboard'),
    
    path('list_of_doctors/', views.list_of_doctors, name="list_of_doctors"),  
    path('view_events/', views.view_events, name="view_events"),  
    path('creating_appointment/', views.creating_appointment, name="creating_appointment"),
    path('appointment_form/', views.appointment_form, name="appointment_form"),  
    path('doctor_details/', views.doctor_details, name="doctor_details"),  
    path('add_doctors_details/', views.add_doctors_details, name="add_doctors_details"),  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
