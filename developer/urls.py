from django.urls import path
from . import views

app_name = "Developer"

urlpatterns = [
    path('info/',views.info,name = 'info'),
    path('join/',views.join, name= 'join'),
    path('update/<int:pk>',views.update, name = 'update'),
    path('myproject/',views.myproject, name = 'myproject'),
    path('follow/',views.follow, name = 'follow'),
]
