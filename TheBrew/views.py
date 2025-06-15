from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, ProfileSerializer,LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile,Log,Menu
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def register(request):
    return render(request, 'register.html')

class RegisterView(APIView):
    def post(self, request):
        user_serializer= UserRegisterSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=400)
        user=user_serializer.save()
        profile=ProfileSerializer(data=request.data, context={'user': user})
        if not profile.is_valid():
            return Response(profile.errors, status=400)
        profile.save()
        return Response({"success":True,"message": "User registered successfully"}, status=201)

def login(request):
    return render(request, 'login.html')

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')

        try:
            get_user = User.objects.get(email=email)
            get_profile = Profile.objects.get(name=get_user)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User not found"}, status=404)
        except Profile.DoesNotExist:
            return Response({"success": False, "message": "Profile not found"}, status=404)
        
        user=authenticate(username=get_user.username, password=password)
        if not user:
            return Response({"success":False,"message": "Invalid credentials"}, status=400)

        serializer= LoginSerializer(data={"account":get_profile.id,"action":"login"})
        if serializer.is_valid():
            serializer.save()

            return Response({
                "id":user.id,
                "success":True,
                "message": "User logged in successfully"
                }, status=200)
        else:
            return Response(serializer.errors, status=400)
        
def edit(request,id):
    user=Profile.objects.get(name__id=id)
    if not user:
        print("User not found")
        return redirect('home')
    return render(request, 'edit.html', {"profile": user})

class EditProfile(APIView):
    def put(self, request, id):
        try:
            profile = Profile.objects.get(name__id=id)
            user= User.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response({"success": False, "message": "Profile not found"}, status=404)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        user_serializer= UserRegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid() and user_serializer.is_valid():
            serializer.save()
            user_serializer.save()
            return Response({"success": True, "message": "Profile updated successfully"}, status=200)
        else:
            return Response(serializer.errors, status=400)
        
class LogoutView(APIView):
    def post(self, request, id):
        try:
            profile = Profile.objects.get(name__id=id)
        except Profile.DoesNotExist:
            return Response({"success": False, "message": "Profile not found"}, status=404)

        serializer = LoginSerializer(data={"account": profile.id, "action": "logout"})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "User logged out successfully"}, status=200)
        else:
            return Response(serializer.errors, status=400)
    
def home(request):
    return render(request, 'home.html')

def profile(request,id):
    user=Profile.objects.get(name__id=id)
    if not user:
        print("User not found")
    return render(request, 'profile.html', {"data": user })

def menu(request):
    menu_items=Menu.objects.all()
    return render(request, 'menu.html',{'menu_items':menu_items})

def point_request(request):
    return render(request, 'point_request.html')
        



