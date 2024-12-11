from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path('info/', views.account_view, name='info'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register'),
]