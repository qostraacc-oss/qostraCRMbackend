from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_onboarded = models.BooleanField(default=False)
    onboarding_step = models.CharField(max_length=50, default='INITIAL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.user_id

    @property
    def is_authenticated(self):
        return True

class Workspace(models.Model):
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='workspaces')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
