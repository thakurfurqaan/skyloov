from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import CartItem, Cart
from cart.serializers import CartItemSerializer, CartItemListSerializer


class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            serializer.save(cart=cart)


class UpdateCartItemQuantityView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def put(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.quantity = request.data.get("quantity", cart_item.quantity)
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)


class CartItemsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart.cart_items.all()


class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
