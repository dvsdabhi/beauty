from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview, CartItem, Customer, ProductAttribute, Attribute

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ('attribute', 'value', 'stock')  # ✅ Add stock field

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'country_of_origin', 'created', 'updated')
    list_filter = ('category', 'country_of_origin', 'created')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductAttributeInline]

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    list_filter = ('rating', 'created')
    search_fields = ('product__name', 'user__name')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Customer)
