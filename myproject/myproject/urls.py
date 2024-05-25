from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def cors_test_view(request):
    return JsonResponse({"message": "CORS is configured correctly."})

urlpatterns = [
    path('api/cors-test/', cors_test_view),
    path('admin/', admin.site.urls),
    path('api/', include('news.urls')),
    path('', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
