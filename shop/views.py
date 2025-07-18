from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from .models import Customer, Product, Category, CartItem, ProductReview
from utils.decorators import customer_login_required
import random
import re
from decimal import Decimal

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
    next_url = request.GET.get('next') or '/'
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
            return redirect(request.POST.get('next') or 'home')
        except Customer.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html', {'next': next_url})

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
    products = Product.objects.all().prefetch_related('images')
    categories = Category.objects.all()
    return render(request, 'shop.html', {'products': products, 'categories': categories})

@customer_login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer_id = request.session.get('customer_id')  # Session-based login system

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        customer = get_object_or_404(Customer, id=customer_id)

        # Optional: prevent duplicate review from same customer
        existing_review = ProductReview.objects.filter(product=product, user=customer).first()
        if existing_review:
            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()
        else:
            ProductReview.objects.create(
                product=product,
                user=customer,
                rating=rating,
                comment=comment
            )

        return redirect('product_detail', id=product_id)

    return redirect('product_detail', id=product_id)

def contact(request):
    return render(request, 'contact.html')

def chackout(request):
    return render(request, 'chackout.html')

# def shopDetail(request):
#     return render(request, 'shop-detail.html')

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop-detail.html', {'product': product})

def testimonial(request):
    return render(request, 'testimonial.html')

@customer_login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, id=request.session['customer_id'])

    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@customer_login_required
def cart_view(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    cart_items = CartItem.objects.filter(customer=customer)
    total = sum(item.total_price() for item in cart_items)
    shipping = Decimal('40.00')  # FIXED: Use Decimal instead of float
    grand_total = total + shipping
    # return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'shipping': 40.00,
        'grand_total': grand_total
    })

@customer_login_required
def update_quantity_ajax(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get("item_id")
        action = request.POST.get("action")

        try:
            item = CartItem.objects.get(id=item_id)
            if action == 'increase':
                item.quantity += 1
            elif action == 'decrease' and item.quantity > 1:
                item.quantity -= 1
            item.save()

            total = sum(i.total_price() for i in CartItem.objects.filter(customer=item.customer))
            shipping = Decimal('40.00')
            grand_total = total + shipping

            return JsonResponse({
                'quantity': item.quantity,
                'item_total': float(item.total_price()),
                'cart_total': float(total),
                'grand_total': float(grand_total),
                "shipping": float(shipping)
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@customer_login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')

def notFound(request):
    return render(request, '404.html')

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