from rest_framework import generics, permissions, serializers
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import CustomUser, UserType
from .serializers import UserSerializer, RegisterSerializer, UserTypeSerializer
from rest_framework import status

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # Remover a criação do token aqui
        }, status=status.HTTP_201_CREATED)

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Invalid credentials",
                "details": serializer.errors,
                "received_data": request.data
            }, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class UserAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserTypeAPI(generics.ListCreateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    permission_classes = [permissions.IsAdminUser]

class UpdateUserTypeAPI(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'user_types' in request.data:
            user_types = UserType.objects.filter(id__in=request.data['user_types'])
            instance.user_types.set(user_types)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class LogoutAPI(KnoxLogoutView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request._auth.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
