from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
  path('',views.IndexView.as_view(), name='index'),
  path('login/', views.MyLoginView.as_view(), name='login'),
  path('logout/', views.MyLogoutView.as_view(), name='logout'),
  path('register/', views.register_user, name='register')
]