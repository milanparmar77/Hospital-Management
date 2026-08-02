from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from doctor.models import Doctor
from .models import Appointment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

@login_required
def appointment_home(request):
    return render(request, 'appointment_home.html')

@login_required
def book_appointment(request):

    if request.method == 'GET':
        doctors = Doctor.objects.all()
        return render(request, 'appointment/book.html', {
            'doctors': doctors
        })

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        patient = request.user.patient

        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        if Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time
        ).exists():
            doctors = Doctor.objects.all()
            return render(request, 'appointment/book.html', {
                'error': 'Slot already booked',
                'doctors': doctors
            })

        try:
            with transaction.atomic():
                Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    date=date,
                    time=time
                )
        except IntegrityError:
            doctors = Doctor.objects.all()
            return render(request, 'appointment/book.html', {
                'error': 'Slot just booked by someone else',
                'doctors': doctors
            })

        return redirect('patient_appointments')
    
@login_required
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id, patient=request.user.patient)

    if appointment.patient.user != request.user:
        return redirect('patient_dashboard')
    
    appointment.status = 'Cancelled'
    appointment.save()

    return redirect('patient_appointments')

@login_required
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id, patient=request.user.patient)

    if appointment.patient.user != request.user:
        return redirect('patient_dashboard')
    
    elif appointment.status == 'Cancelled':
        appointment.delete()
    
    else:
        messages.error(request, 'First Calcel the Appointment then you can delete it.')

    return redirect('patient_appointments')