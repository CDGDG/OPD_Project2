from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = "Developer"

urlpatterns = [
    path('info/',views.info,name = 'info'),
    path('join/',views.join, name= 'join'),
    path('check_id/',views.check_id, name='check_id'),
    path('check_nick/',views.check_nick, name='check_nick'),
    path('logout/',views.logout,name="logout"),
    path('update/<int:pk>',views.update, name = 'update'),
    path('myproject/',views.myproject, name = 'myproject'),
    path('follow/',views.follow, name = 'follow'),
    path('login/', views.login, name='login'),
]
