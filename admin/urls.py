from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "Admin"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/',views.check_userid, name="forgot_password"),
    path('reset_password/', views.OPD_PasswordResetView.as_view(), name ='reset_password'),
    path('reset_password_done/', views.OPD_PasswordResetDoneView.as_view(), name ='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    
]
