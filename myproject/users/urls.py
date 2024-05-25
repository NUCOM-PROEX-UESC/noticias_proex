from django.urls import path
from knox import views as knox_views
from .views import RegisterAPI, LoginAPI, UserAPI, UserTypeAPI, UpdateUserTypeAPI, LogoutAPI

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', LogoutAPI.as_view(), name='logout'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/usertypes/', UserTypeAPI.as_view(), name='usertypes'),
    path('api/usertypes/update/<int:pk>/', UpdateUserTypeAPI.as_view(), name='update_usertype'),
]
