from rest_framework import serializers

from .models import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), write_only=True)
    product_category_data = ProductCategorySerializer(source="category", read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'product_category_data', 'category']

