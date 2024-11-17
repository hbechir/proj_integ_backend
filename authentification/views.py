# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny

from .utils import send_code_to_phone,generate_verification_code
import datetime


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    
    if not phone_number or not password:
        return Response({"error": "Phone number and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=phone_number, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Successfully logged in."}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_phone_number(request):
    '''Checks if the phone number is already registered, if not, sends a code to the phone number and saves it in the session'''
    
    phone_number = request.data.get('phone_number')
    
    # Check if phone number is already registered
    if User.objects.filter(username=phone_number).exists():
        return Response({"error": "Phone number is already registered."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate and send verification code
    code = generate_verification_code()
    send_code_to_phone(phone_number, code)
    
    # Store verification code in session
    request.session['verification_code'] = code
    request.session['phone_number_verified'] = False
    request.session['phone_number'] = phone_number
    request.session['code_generated_at'] = str(datetime.datetime.now())  # For expiration check
    
    return Response({"message": "Code sent to phone number."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    verification_code = request.data.get('verification_code')
    if not verification_code:
        return Response({"error": "Verification code is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'verification_code' not in request.session:
        return Response({"error": "No verification code sent."}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.session['verification_code'] != verification_code:
        return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
    
    request.session['phone_number_verified'] = True
    
    return Response({"message": "Code verified."}, status=status.HTTP_200_OK)






@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    phone_number = request.session['phone_number']
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')
    
    
    
    # to use serializer later ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
    
    if not password or not password_confirm:
        return Response({"error": "Password and password confirmation are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if password != password_confirm:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'phone_number_verified' not in request.session or not request.session['phone_number_verified']:
        return Response({"error": "Phone number not verified."}, status=status.HTTP_400_BAD_REQUEST)
    



    

    
    