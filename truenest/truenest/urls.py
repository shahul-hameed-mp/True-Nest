"""
URL configuration for truenest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.Home.as_view(), name="home_view"),
    path('register', views.UserRegisterView.as_view(), name="register"),
    path('login', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileListView.as_view(), name='profile_view'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('properties/all/', views.PropertiesAllView.as_view(), name='properties_all'),
    path('properties/buy/', views.properties_buy, name='properties_buy'),
    path('properties/rent/', views.properties_rent, name='properties_rent'),
    path('property/<int:pk>/',views.PropertyDetailView.as_view(), name='property_detail'),
    path('favorites/', views.FavoritesListView.as_view(), name='favorites_list'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/add/', views.PropertyCreateView.as_view(), name='property_add'),
    path('properties/<int:pk>/edit/', views.PropertyUpdateView.as_view(), name='property_edit'),
    path('properties/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='property_delete'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
