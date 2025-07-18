from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update-quantity/', views.update_quantity_ajax, name='update_quantity_ajax'),
    path('remove-cart-item/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('contact/', views.contact, name='contact'),
    path('chackout/', views.chackout, name='chackout'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
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