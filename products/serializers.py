from rest_framework import serializers
from products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "thumbnail", "small", "large"]


class ProductImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "images"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "category",
            "brand",
            "created_at",
            "updated_at",
            "rating",
            "images",
        ]


class ProductSearchSerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_blank=True)
    brand = serializers.CharField(required=False, allow_blank=True)
    min_price = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2
    )
    max_price = serializers.DecimalField(
        required=False, max_digits=10, decimal_places=2
    )
    min_quantity = serializers.IntegerField(required=False)
    max_quantity = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)
