from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('django/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
]
