from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .serializers import UserSerializer, UserDetailSerializer, FollowSerializer
from .models import User, Follow
from .utils import send_verification_email, verify_email_token, resend_verification_email

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification email
        if send_verification_email(user):
            return Response({
                'message': 'ثبت نام با موفقیت انجام شد. لطفاً ایمیل خود را برای تایید بررسی کنید.',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        else:
            # If email sending fails, still create user but inform about email issue
            return Response({
                'message': 'ثبت نام انجام شد اما ارسال ایمیل تایید با مشکل مواجه شد. لطفاً با پشتیبانی تماس بگیرید.',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'نام کاربری و رمز عبور الزامی است.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            if not user.is_active:
                return Response({
                    'error': 'حساب کاربری شما فعال نیست. لطفاً ایمیل خود را تایید کنید.',
                    'needs_verification': True,
                    'email': user.email
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not user.is_email_verified:
                return Response({
                    'error': 'ایمیل شما تایید نشده است. لطفاً ایمیل خود را تایید کنید.',
                    'needs_verification': True,
                    'email': user.email
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserDetailSerializer(user).data
            })
        
        return Response({
            'error': 'نام کاربری یا رمز عبور اشتباه است.'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    """
    Resend verification email
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'ایمیل الزامی است.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    success, message = resend_verification_email(email)
    
    if success:
        return Response({
            'message': message
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': message
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    """
    Verify email with token
    """
    success, message = verify_email_token(token)
    
    if success:
        return Response({
            'message': message,
            'verified': True
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': message,
            'verified': False
        }, status=status.HTTP_400_BAD_REQUEST)

def verify_email_page(request, token):
    """
    Render email verification page
    """
    success, message = verify_email_token(token)
    
    if success:
        return render(request, 'users/email_verification_success.html', {
            'message': message,
            'verified': True
        })
    else:
        return render(request, 'users/email_verification_success.html', {
            'error': message,
            'verified': False
        })

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
