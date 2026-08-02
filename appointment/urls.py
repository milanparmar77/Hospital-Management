from django.urls import path 
from . import views

urlpatterns = [
    path('', views.appointment_home),
    path('book/', views.book_appointment, name='book_appointment'),
    path('cancel/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
    path('delete/<int:id>/', views.delete_appointment, name='delete_appointment')

]