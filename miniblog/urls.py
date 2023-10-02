"""
URL configuration for miniblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homeview),
    path('about/',views.aboutview,name='about'),
    path('changepass/',views.change_password,name='changepass'),
    path('contact/',views.contactview,name='contact'),
    path('dashboard/',views.dashboardview,name='dashboard'),
    path('signup/',views.signupview,name='signup1'),
    path('login/',views.loginview,name='login'),
    path('logout/',views.logoutview,name='logout'),
    path('addpost/',views.addpost,name='addpost'),
    path('addpost2/',views.addpost2,name='addpost2'),
    path('updatepost/<int:id>/',views.updatepost,name='updatepost'),
    path('delete/<int:id>/',views.deletepost,name='delete'),
    path('verify/<str:token>',views.verify,name='verify'),
    path('profile/',views.profielview,name='profile'),
    path('updateprofile/<int:id>',views.updateprofile,name='upateprofile'), 
    path('api/',include('blog.api.urls')),
]
