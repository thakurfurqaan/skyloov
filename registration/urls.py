from django.urls import path
from registration.views import UserCreate

urlpatterns = [
    path("", UserCreate.as_view(), name="account-create"),
]
