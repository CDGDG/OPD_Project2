from unicodedata import name
from django.urls import path
from .import views

app_name = "Board"

urlpatterns = [
    path("list/", views.board_list, name="list"),
    path("create/", views.board_create, name="create"),
    path("detail/<int:pk>/", views.board_detail, name="detail"),
    path("update/<int:pk>/", views.board_update, name="update"),
    path("delete/", views.board_delete, name="delete"),
    path("filedownload/<int:pk>/", views.filedownload, name='filedownload'),
    path('commentwrite/<int:pk>/', views.comment_write, name='commentwrite'),
    path('commentdelete/', views.comment_delete, name='commentdelete'),
    # path("c")
]
