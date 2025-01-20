from django.urls import path
from . import views

urlpatterns = [
    path(r'user/', views.UserList.as_view({"get": "list"}), name="Get User List"),
    path(r'user/create/', views.UserCreate.as_view({"post": "create"}), name="Create One User"),
    path(r'user/delete/', views.UserDelete.as_view({"post": "create"}), name="Delete One User"),
]
