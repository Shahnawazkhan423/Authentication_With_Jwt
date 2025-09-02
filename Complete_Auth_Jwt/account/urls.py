from django.urls import path,include
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordEmail,UserPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(),name='changepassword'),
    path('reset/',SendPasswordEmail.as_view(),name='reset'),
    path('user-reset/<uid>/<token>/',UserPasswordResetView.as_view(),name='user-reset'),

]
