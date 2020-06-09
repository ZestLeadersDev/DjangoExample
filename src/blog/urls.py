from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'blog'

urlpatterns = [
    #path('', views.post_list, name='post_list'),
    path('<int:day>/<int:month>/<int:year>/<slug:post>/', views.post_detail, name='post_detail'),
    path('', views.test, name='test'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
