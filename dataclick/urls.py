from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    re_path('^', include('analyzeapp.urls', namespace='analyze')),
    re_path('^tasks/', include('tasksapp.urls', namespace='tasks')),

    path('admin/', admin.site.urls),
]
