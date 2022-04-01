from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('developer/',include('developer.urls')),
    path('project/', include('project.urls')),
    path('company/', include('company.urls')),
]
