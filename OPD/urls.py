from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from admin.views import home

urlpatterns = [
    path('admin/',include('admin.urls')),
    path('developer/',include('developer.urls')),
    path('project/', include('project.urls')),
    path('board/', include('board.urls')),
    path('company/', include('company.urls')),
    path('recruit/', include('recruit.urls')),
    path('', home, name='home'),
]

# MEDIA 경로 추가
urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
)
