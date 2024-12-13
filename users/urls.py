from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.user_view, name='user'),
    path('update/', views.update_view, name='update'),
    path('delete/', views.delete_view, name='delete'),
    path('register/', views.register_view, name='register'),
]