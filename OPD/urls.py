from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',include('admin.urls')),
    path('developer/',include('developer.urls')),
    path('project/', include('project.urls')),
    path('board/', include('board.urls')),
    path('company/', include('company.urls')),
]
