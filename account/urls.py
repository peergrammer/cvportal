from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [    
    path('', views.panel, name='panel'),
    path('', include('django.contrib.auth.urls')),  # use the Django Authentication Views
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('panel/', views.panel, name='panel'),
    path('education/', views.education_post, name ='education'),
    path('attachment/', views.attachment_post, name ='attachment'),
]
