from django.urls import path

from products.views import (
    ProductSearchView,
    ProductDetail,
    upload_product_image,
)

urlpatterns = [
    path("search/", ProductSearchView.as_view(), name="product_search"),
    path("<int:pk>/upload-image/", upload_product_image, name="upload_product_image"),
    path("<int:pk>/", ProductDetail.as_view(), name="product"),
    path("", ProductDetail.as_view()),
]
