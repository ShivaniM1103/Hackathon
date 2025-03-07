from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        # print("Received Data:", request.data)  # Debugging
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        print("Errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        # print("Received data:", request.data)  # Debugging print
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(username=username)

                if user.check_password(password):  # Manually verify password
                    login(request, user)  # Log the user in

                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "role": user.role
                    })

                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        print("Serializer errors:", serializer.errors)  # Debugging print
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Log out the user
            logout(request)

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Invalid token or already logged out"}, status=status.HTTP_400_BAD_REQUEST)