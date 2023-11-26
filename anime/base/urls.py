from django.urls import path
from . import views


urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logoutuser'),
    path('register/',views.registerPage,name='register'),
    path('',views.Home,name="home"),
    path('profile/<str:pk>',views.userProfile, name="user-profile"),
    path('update-user/',views.updateUser,name='update-user'),
    path('updates/',views.notification,name='updates'),


    path('shop/', views.shop, name='shop' ),
    path('shop/cart/',views.cart,name="cart"),
    path('shop/checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('shop/payment/',views.payment,name="payment"),
    path('shop/confirmed_pay/',views.payment_confirmed, name='payment_confirmed'),


    #Samin Rahman
    path('Event/', views.index, name='all_socialize'),
    path('Event/<slug:socializes_slug>/success', views.registration_complete, name='reg_com'),
    # our-domain.com/socialize
    path('Event/<slug:socializes_slug>', views.socializes_details, name='socializes-details'), # our-domain.com/socialize/<dynamic-path-segment>a-second-socialize
    # path('#')

]
