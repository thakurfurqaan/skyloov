from django.urls import path
from . import views

urlpatterns = [
    # View all cart items for the authenticated user
    path("items/", views.CartItemsView.as_view(), name="cart_items"),
    # Add a product to the cart for the authenticated user
    path("items/add/", views.AddToCartView.as_view(), name="add_to_cart"),
    # Update the quantity of a cart item for the authenticated user
    path(
        "items/<int:pk>/quantity/",
        views.UpdateCartItemQuantityView.as_view(),
        name="update_cart_item_quantity",
    ),
    # Remove a cart item from the authenticated user's cart
    path(
        "items/<int:pk>/remove/",
        views.RemoveCartItemView.as_view(),
        name="remove_cart_item",
    ),
]
