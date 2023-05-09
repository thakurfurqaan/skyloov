import os
import multiprocessing
from PIL import Image

from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend

from products.serializers import (
    ProductSearchSerializer,
    ProductSerializer,
)
from products.serializers import ProductImageSerializer
from products.models import Product, ProductImage
from products.tasks import process_product_image


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        product = self.get_object()

        images = request.FILES.getlist("images")
        if not images:
            return Response(
                {"detail": "No images provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        for image in images:
            product_image = ProductImage(product=product, image=image)
            product_image.save()

        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "category": ["exact"],
        "brand": ["exact"],
        "price": ["gte", "lte"],
        "quantity": ["gte", "lte"],
        "created_at": ["exact", "gte", "lte"],
        "rating": ["exact", "gte", "lte"],
    }
    ordering_fields = ["price", "rating", "created_at", "quantity"]

    def get_queryset(self):
        queryset = Product.objects.all()
        search_params = ProductSearchSerializer(data=self.request.query_params)
        search_params.is_valid(raise_exception=True)
        queryset = self.filter_queryset(queryset)
        return queryset


def process_image(image_path, size):
    image = Image.open(image_path)
    image.thumbnail(size)
    new_image_path = os.path.join(
        os.path.dirname(image_path),
        f"{size[0]}x{size[1]}",
        os.path.basename(image_path),
    )
    os.makedirs(os.path.dirname(new_image_path), exist_ok=True)
    image.save(new_image_path)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_product_image(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Get the list of images from the request
    images = request.FILES.getlist("images", [])

    # Iterate through each image and create a ProductImage instance for it
    product_image_ids = []
    for image in images:
        serializer = ProductImageSerializer(data={"image": image})
        if serializer.is_valid():
            # Save the ProductImage instance with the product reference
            product_image = serializer.save()
            product.images.add(product_image)
            product_image_ids.append(product_image.id)
            product.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    for product_image_id in product_image_ids:
        process = multiprocessing.Process(
            target=process_product_image, args=(product_image_id,)
        )
        process.start()

    return Response(status=status.HTTP_201_CREATED)
