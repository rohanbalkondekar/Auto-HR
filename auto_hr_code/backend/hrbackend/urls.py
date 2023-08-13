from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', include('postjobs.urls')),  # Include the URL patterns from the postjobs app
]
