from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointment.models import Appointment
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import traceback

@login_required
def doctor_home(request):
    doctor = request.user.doctor
    total_patients = Appointment.objects.filter(
        doctor = doctor
    ).values('patient').distinct().count()

    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=date.today()
    ).count()

    return render(request, 'doctor/doctor_home.html', {
        'total_patients': total_patients,
        'today_appointments': today_appointments
    })

@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor

    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).values('patient').distinct().count()

    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=date.today()
    ).count()

    pending_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='Pending'
    ).count()

    appointments = Appointment.objects.filter(doctor=doctor).order_by('-id')

    paginator = Paginator(appointments, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'doctor/doctor_dashboard.html',  {
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'appointments': appointments,
        'page_obj': page_obj,
    })


    
@login_required
def update_status(request, id):
    try:
        appointment = get_object_or_404(Appointment, id=id)

        if request.method == "POST":
            action = request.POST.get('action')

            print("ACTION:", action)
            print("BEFORE:", appointment.status)

            if action == "approve":
                appointment.status = "Approved"

            elif action == "reject":
                appointment.status = "Cancelled"
            
            elif action == 'complete':
                appointment.status = 'Completed'

            appointment.save()

            print("AFTER SAVE:", appointment.status)

    except Exception as e:
        print("ERROR OCCURRED:")
        traceback.print_exc()

    return redirect('doctor_dashboard')
