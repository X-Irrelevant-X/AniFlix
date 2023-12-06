from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logoutuser'),
    path('register/',views.registerPage,name='register'),
    path('',views.Home,name="home"),
    path('profile/<str:pk>',views.userProfile, name="user-profile"),
    path('update-user/',views.updateUser,name='update-user'),
    path('updates/<str:pk>',views.notification,name='updates'),
    path('genre/',views.genre_list, name='genre'),
    path('favorites/', views.favorite_anime, name='favorites'),
    path('remove_from_favorites/<int:anime_id>/', views.remove_from_favorites, name='remove-from-favorites'),
    path('toggle_favorite/<int:anime_id>/', views.toggle_favorite, name='toggle_favorite'),


    path('shop/', views.shop, name='shop' ),
    path('shop/cart/',views.cart,name="cart"),
    path('shop/checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('shop/payment/',views.payment,name="payment"),
    path('shop/confirmed_pay/<str:pk>',views.payment_confirmed, name='payment_confirmed'),
    path('shop/orders/', views.order_history, name='orders'),
    path('shop/recipt/<int:pk>',views.recipt,name="recipt"),


    path('Event/', views.index, name='all_socialize'),
    path('Event/<slug:socializes_slug>/success', views.registration_complete, name='reg_com'),
    path('Event/<slug:socializes_slug>', views.socializes_details, name='socializes-details'),
   
   #Streaming URL
    path('streaming/anime/<int:pk>/', views.anime_detail, name='anime-detail'),
    path('streaming/episode/<int:pk>/', views.episode_detail, name='episode-detail'),
    path('streaming/delete_comment/<int:pk>/',views.delete_comment, name='delete-comment'),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)