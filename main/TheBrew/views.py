from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, ProfileSerializer,LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile,Log,Menu
from rest_framework.permissions import AllowAny
from .models import PointRequest,PointRequest_Image,Notification,Promotion,Reward,ClaimedReward
from django.http import JsonResponse
from datetime import date
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

def point_request_add_data(request,id):
    if request.method == 'POST':
        user=Profile.objects.get(name__id=id)
        points_requested = request.POST.get('points_requested')
        image = request.FILES.get('image')

        if not points_requested or not image:
            return render(request, 'point_request.html', {"error": "All fields are required."})
        
        point_request = PointRequest.objects.create(
            account=user,
            points_requested=points_requested,
        )
        point_request.save()

        if 'image' in request.FILES:
            point_request_image = PointRequest_Image.objects.create(
                image=image,
                request=point_request
            )
            point_request_image.save()

        return JsonResponse({
            "success": True,
            "message": "Point request added successfully",
            "point_request_id": point_request.id
        }, status=201)
    return JsonResponse({
        "success": False,
        "message": "Invalid request method"
    }, status=405)

def notifications(request, id):
    user = get_object_or_404(Profile, name__id=id)
    notifications = Notification.objects.filter(account=user).order_by('-created_at')
    return render(request, 'notifications.html', {"notifications": notifications})
        
def promotions(request,id=None):
    if id :
        user=get_object_or_404(Profile, name__id=id)
        if user.status=="diamond":
            promotions=Promotion.objects.filter(expired_date__gte=date.today())
        else:
            promotions=Promotion.objects.filter(audience='everyone',expired_date__gte=date.today())        
    else:
        promotions=Promotion.objects.filter(audience='everyone',expired_date__gte=date.today())

    return render(request,'promotion.html',{"promotions":promotions} )

def rewards(request):
    rewards=Reward.objects.all()
    return render(request,'rewards.html',{"rewards":rewards})

def claimRewards(request,userId,rewardId):
    profile=Profile.objects.get(name__id=userId)
    reward=Reward.objects.get(pk=rewardId)

    if profile.points >= reward.points_required:
        profile.points -= reward.points_required
        profile.save()

        ClaimedReward.objects.create(profile=profile,reward=reward)

        return JsonResponse({
            "success":True,
            "message":"You have redeemed the reward successfully"
        })
    else:
        return JsonResponse({
            "success":False,
            "message":"You don't have enough points"
        })

def storage(request,id):
    user=Profile.objects.get(name__id=id)
    history=ClaimedReward.objects.filter(profile=user)
    return render(request,"storage.html",{"history":history})

