from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "Developer"

urlpatterns = [
    path('join/',views.join, name= 'join'),
    path('check_id/',views.check_id, name='check_id'),
    path('check_nick/',views.check_nick, name='check_nick'),
    path('check/password/',views.checkPassword,name="checkPassword"),
    path('send_email/',views.send_email, name='send_email'),
    path('info/<int:pk>/',views.info,name = 'info'),
    path('download/<int:pk>/',views.download, name ='resume_download'),
    path('update/',views.update, name = 'update'),
    path('myproject/<int:pk>/',views.myproject, name = 'myproject'),
    path('follow/',views.myfollowers, name = 'followers'),  # 내 팔로우 리스트
    path('follower/',views.follow, name = 'follow'), # 팔로우 하기
    path('list/',views.list, name = 'list'),
    path('leave/',views.leave, name = 'leave'),
]

#MEDIA 경로 추가
urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)