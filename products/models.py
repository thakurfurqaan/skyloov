from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    rating = models.FloatField()
    images = models.ManyToManyField("ProductImage", related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/images")
    thumbnail = models.ImageField(upload_to="products/thumbnails", null=True)
    small = models.ImageField(upload_to="products/small", null=True)
    large = models.ImageField(upload_to="products/large", null=True)

    def __str__(self):
        return f"{self.image}"
