from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_home, name='doctor_home'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),
]