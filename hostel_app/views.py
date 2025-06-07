from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, StudentForm
from .models import Student, BookingRequest
from .models import Room, BookingRequest
from django.contrib import messages
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required
from .models import Student, Payment



def home(request):
    return render(request, 'hostel_app/home.html')

@login_required
def roommate_suggestions(request):
    student = Student.objects.get(user=request.user)

    try:
        booking = BookingRequest.objects.get(student=student, status="Approved")
    except BookingRequest.DoesNotExist:
        messages.warning(request, "You must have an approved booking to see roommate suggestions.")
        return redirect('student_dashboard')

    # Same room, same branch, same year but not the student themself
    suggestions = Student.objects.filter(
        bookingrequest__preferred_room=booking.preferred_room,
        bookingrequest__status="Approved",
        department=student.department,
        year=student.year
    ).exclude(id=student.id)

    return render(request, 'hostel_app/roommate_suggestions.html', {
        'suggestions': suggestions,
        'room': booking.preferred_room
    })

@staff_member_required
def verify_payments(request):
    payments = Payment.objects.all().order_by('-date')

    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        payment = Payment.objects.get(id=payment_id)
        payment.status = "Paid"
        payment.save()
        return redirect('verify_payments')

    return render(request, 'hostel_app/verify_payments.html', {'payments': payments})


@login_required
def submit_payment(request):
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        Payment.objects.create(student=student, amount=amount)
        messages.success(request, "Payment submitted! Awaiting admin verification.")
        return redirect('student_dashboard')

    return render(request, 'hostel_app/submit_payment.html')
   



@staff_member_required
def admin_dashboard(request):
    requests = BookingRequest.objects.all().order_by('-id')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        booking_request = BookingRequest.objects.get(id=request_id)

        if action == 'approve':
            room = booking_request.preferred_room
            if room.current_occupancy < room.capacity:
                room.current_occupancy += 1
                room.save()
                booking_request.status = 'Approved'
                booking_request.save()
            else:
                messages.warning(request, 'Room is already full!')
        elif action == 'reject':
            booking_request.status = 'Rejected'
            booking_request.save()

        return redirect('admin_dashboard')

    return render(request, 'hostel_app/admin_dashboard.html', {'requests': requests})


@login_required
def book_room(request):
    student = Student.objects.get(user=request.user)

    # Prevent double booking
    if BookingRequest.objects.filter(student=student).exists():
        messages.warning(request, "You have already submitted a booking request.")
        return redirect('student_dashboard')

    available_rooms = Room.objects.filter(current_occupancy__lt=models.F('capacity'))

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        selected_room = Room.objects.get(id=room_id)

        BookingRequest.objects.create(
            student=student,
            preferred_room=selected_room,
            status='Pending'
        )
        messages.success(request, "Booking request submitted successfully!")
        return redirect('student_dashboard')

    return render(request, 'hostel_app/book_room.html', {
        'available_rooms': available_rooms
    })


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        student_form = StudentForm()
    return render(request, 'hostel_app/register.html', {'user_form': user_form, 'student_form': student_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('student_dashboard')
        else:
            return render(request, 'hostel_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'hostel_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.models import User

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    booking = BookingRequest.objects.filter(student=student).first()

    is_admin = request.user.is_staff  # or use custom logic if you have a specific admin flag

    return render(request, 'hostel_app/student_dashboard.html', {
        'student': student,
        'booking': booking,
        'is_admin': is_admin,  # pass this to template
    })

