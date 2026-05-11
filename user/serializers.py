from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    user_info = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'user_info', 'name', 'description', 
            'price', 'sku', 'stock_quantity', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_info', 'created_at', 'updated_at']
