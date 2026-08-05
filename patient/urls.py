from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_home, name='patient_home'),
    # path('home/', views.patient_home, name='patient_home'),
    path('appointment/', views.patient_appointments, name='patient_appointments'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]   

