from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Customer
import random
import re

# Create your views here.

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        otp = str(random.randint(100000, 999999))
        customer = Customer(name=name, email=email, password=password, otp=otp)
        customer.save()

        send_mail(
            subject="Email Verification OTP",
            message=f"Your OTP is: {otp}",
            from_email="divyeshd623@gmail.com",
            recipient_list=[email],
        )

        request.session['email'] = email
        messages.success(request, "OTP sent to your email.")
        return redirect('verify_otp')

    return render(request, 'register.html')

def verify_otp(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        try:
            customer = Customer.objects.get(email=email)
            if customer.otp == entered_otp:
                customer.is_verified = True
                customer.otp = ''
                customer.save()
                messages.success(request, "Email verified successfully. Please login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP.")
        except Customer.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'verify_otp.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email, password=password)
            if not customer.is_verified:
                messages.error(request, "Please verify your email first.")
                return redirect('verify_otp')

            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.name
            messages.success(request, f"Welcome {customer.name}")
            return redirect('home')
        except Customer.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def Forgot_Password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            customer = Customer.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            customer.otp = otp
            customer.save()

            send_mail(
                subject='Password Reset OTP',
                message=f'Your OTP to reset password is: {otp}',
                from_email='divyeshd623@gmail.com',
                recipient_list=[email]
            )

            request.session['reset_email'] = email
            messages.success(request, "OTP sent to your email.")
            return redirect('reset_password')
        except Customer.DoesNotExist:
            messages.error(request, "Email not found.")
    return render(request, 'forgot_password.html')

def reset_password(request):
    email = request.session.get('reset_email')

    if not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect('forgot_password')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        # Custom password validation (min 8 chars, letter+number)
        if len(new_password) < 8 or not re.search(r'[A-Za-z]', new_password) or not re.search(r'\d', new_password):
            messages.error(request, "Password must be at least 8 characters long and include both letters and numbers.")
            return redirect('reset_password')

        try:
            customer = Customer.objects.get(email=email)
            if customer.otp == entered_otp:
                customer.password = new_password
                customer.otp = ''
                customer.save()
                del request.session['reset_email']  # cleanup
                messages.success(request, "Password reset successful. Please login.")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP.")
        except Customer.DoesNotExist:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('forgot-password')

    return render(request, 'reset_password.html')

def shop(request):
    return render(request, 'shop.html')

def contact(request):
    return render(request, 'contact.html')

def chackout(request):
    return render(request, 'chackout.html')

def shopDetail(request):
    return render(request, 'shop-detail.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def cart(request):
    return render(request, 'cart.html')

def notFound(request):
    return render(request, '404.html')

from django.core.mail import send_mail
import random
from .models import Customer
from django.contrib import messages

def resend_otp(request):
    email = request.session.get('email')  # stored in session during register

    if not email:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')

    try:
        customer = Customer.objects.get(email=email)
        otp = str(random.randint(100000, 999999))
        customer.otp = otp
        customer.save()

        send_mail(
            subject='Resend OTP - Email Verification',
            message=f'Your OTP is: {otp}',
            from_email='divyeshd623@gmail.com',
            recipient_list=[email]
        )

        messages.success(request, "OTP resent to your email.")
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")

    return redirect('verify_otp')

def account(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    customer = Customer.objects.get(id=customer_id)
    return render(request, 'account.html', {'customer': customer})