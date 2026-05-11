from django.contrib import admin
from .models import UserInfo, Product

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'company_name', 'created_at')
    search_fields = ('user_id', 'email', 'first_name', 'last_name', 'company_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock_quantity', 'user_info', 'is_active')
    search_fields = ('name', 'sku', 'user_info__user_id')
    list_filter = ('is_active', 'created_at')
