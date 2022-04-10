from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "Admin"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.adminlogin, name='adminlogin'),
    path('notice/list/', views.noticelist, name='noticelist'),
    path('notice/write/', views.noticewrite, name='noticewrite'),
    path('notice/delete/', views.noticedelete, name='noticedelete'),
    path('notice/detail/<int:pk>/', views.noticedetail, name='noticedetail'),
    path('forgot_password/',views.check_userid, name="forgot_password"),
    path('reset_password/', views.OPD_PasswordResetView.as_view(), name ='reset_password'),
    path('reset_password_done/', views.OPD_PasswordResetDoneView.as_view(), name ='password_reset_done'),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    path('language/', views.language, name='language'),
    path('language/add/', views.languageadd, name='languageadd'),
    path('language/delete/', views.languagedelete, name='languagedelete'),
    path('notice/filedownload/<int:pk>/', views.filedownload, name='filedownload'),
    
]
