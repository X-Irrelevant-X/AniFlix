from django.urls import path
from . import views


urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logoutuser'),
    path('register/',views.registerPage,name='register'),
    path('',views.Home,name="home"),
    path('profile/<str:pk>',views.userProfile, name="user-profile"),
    path('update-user/',views.updateUser,name='update-user'),
    path('shop/', views.shop, name='shop' ),
]