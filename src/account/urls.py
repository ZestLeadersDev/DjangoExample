from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import ajax
from . import views
from .forms import EmailValidationOnForgotPassword

app_name = 'account'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('register/check_email/', ajax.check_email, name='check_email'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email_template.html',
        subject_template_name='account/password_reset_email_subject.txt',
        success_url=reverse_lazy('account:password_reset_done'),
        form_class=EmailValidationOnForgotPassword),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # profile edit
    path('edit/', views.profile_edit, name='edit'),
]
