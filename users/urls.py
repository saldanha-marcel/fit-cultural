from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user_view, name='create_user'),
    path("list/", views.list_users_view, name="list_users"),
    path("edit/<int:user_id>/", views.edit_user_view, name="edit_user"),
    path("delete/<int:user_id>/", views.delete_user_view, name="delete_user"),
]
