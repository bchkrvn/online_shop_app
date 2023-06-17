from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm, CustomSetPasswordForm

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', login_required(views.UserView.as_view()), name='user_detail'),
    path('me/edit/', login_required(views.UserEditView.as_view()), name='user_edit'),
    path("login/", auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('me/delete/', login_required(views.UserDeleteView.as_view()), name='user_delete'),

    path("me/edit/password_change/", login_required(auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy("users:password_change_done"),
        form_class=CustomPasswordChangeForm)), name="password_change"),
    path("me/edit/password_change/done/", login_required(auth_views.PasswordChangeDoneView.as_view()),
         name="password_change_done"),

    path("password_reset/", auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy("users:password_reset_done")), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy("users:password_reset_complete"),
        form_class=CustomSetPasswordForm), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
