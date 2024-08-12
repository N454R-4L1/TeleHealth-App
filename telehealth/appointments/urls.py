from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
      path('register/', views.register, name='register'),
      path('login/', views.login_view, name='login'),
      path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
      path('schedule/', views.schedule_appointment, name='schedule_appointment'),
      path('appointments/', views.view_appointments, name='view_appointments'),
      path('video/', views.video_call, name='video_call'),
      path('chat/', views.chat, name='chat'),
      path('checkout/', views.checkout, name='checkout'),
      path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]
