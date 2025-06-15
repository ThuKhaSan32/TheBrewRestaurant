from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns= [
    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('login/', views.login, name='login'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
    path('logout/<int:id>/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:id>/',views.profile, name='profile'),
    path('point_request/', views.point_request, name='point_request'),
    path('edit/<int:id>/',views.edit,name='editprofile'),
    path('api/edit/<int:id>/', views.EditProfile.as_view(), name='api_edit_profile'),
    path('menu/',views.menu, name='menu'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)