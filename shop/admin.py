from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview, CartItem, Customer

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'country_of_origin', 'created', 'updated')
    list_filter = ('category', 'country_of_origin', 'created')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    list_filter = ('rating', 'created')
    search_fields = ('product__name', 'user__name')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Customer)
