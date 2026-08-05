from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from appointment.models import Appointment
from .models import Patient
from .forms import EditProfileForm
from django.contrib import messages

@login_required
def patient_home(request):
    return render(request, 'patient/patient_home.html')

@login_required
def patient_dashboard(request):

    patient = request.user.patient

    total_appointments = Appointment.objects.filter(
        patient=patient
    ).count()

    approved_appointments = Appointment.objects.filter(
        patient=patient,
        status='Approved'
    ).count()

    pending_appointments = Appointment.objects.filter(
        patient=patient,
        status='Pending'
    ).count()

    completed_appointments = Appointment.objects.filter(
        patient=patient,
        status='Completed'
    ).count()

    recent_appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-id')[:5]


    context = {
        'total_appointments': total_appointments,
        'approved_appointments': approved_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'recent_appointments': recent_appointments,
    }

    return render(request, 'patient/patient_dashboard.html', context)

@login_required
def patient_appointments(request):
    patient = request.user.patient

    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'patient/appointments.html', {
        'appointments': appointments
    })

@login_required
def edit_profile(request):
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)

        if form.is_valid():
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.email = form.cleaned_data["email"]
            request.user.save()

            Patient.phone = form.cleaned_data["phone"]

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("edit_profile")

        return render(request, "patient/edit_profile.html", {"form": form})
    
    return render(request, "patient/edit_profile.html", {})

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user.patient
    )

    if appointment.status in ['Pending', 'Approved']:
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, "Your appointment has been cancelled successfully.")

    return redirect('view_appointments')
