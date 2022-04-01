from django.urls import path
from .import views

app_name = "Board"

urlpatterns = [
    path("list/", views.board_list, name="list"),
    path("create/", views.board_create, name="create"),
    path("detail/<int:pk>/", views.board_detail, name="detail"),
    path("update/<int:pk>/", views.board_update, name="update"),
]
