from django.db import models
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.email

# Category Table
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Product Table
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('ltr', 'Litre'),
        ('ml', 'Millilitre'),
        ('pcs', 'Pieces'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='kg')
    country_of_origin = models.CharField(max_length=100, default="India")
    bullet_points = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_bullet_points(self):
        return [point.strip() for point in self.bullet_points.split(',') if point.strip()]

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0


# Product Image Table (Many-to-One)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} Image"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)  # range: 1 to 5
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"


# Cart Item Table
class CartItem(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"
