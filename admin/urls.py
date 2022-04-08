from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "Admin"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('checkuserid/',views.check_userid, name="check_userid"),
    path('resetpassword/',views.reset_password, name="resetpassword"),
    # path('reset_password/', views.OPD_PasswordResetView.as_view(), name ='reset_password'),
    # path('reset_password_done/', views.OPD_PasswordResetDoneView.as_view(), name ='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    
]
