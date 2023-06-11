from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', login_required(views.UserView.as_view()), name='user_detail'),
    path('me/edit/', login_required(views.UserEditView.as_view()), name='user_edit'),
]