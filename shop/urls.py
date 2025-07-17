from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('chackout/', views.chackout, name='chackout'),
    path('shop<int:pk>/', views.shopDetail, name='shop-detail'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('404/', views.notFound, name='notFound'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.Forgot_Password, name='forgot-password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('account/', views.account, name='account'),
]