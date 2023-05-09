from django.contrib import admin
from products.models import Product, ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "category", "brand", "rating")
    ordering = ("name",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
