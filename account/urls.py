from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView ,  TokenRefreshView


# Internal 
from account.views import ( UserRegistrationView, UserLoginview, UserProfileView, UserChangepasswordView , SendPasswordRestEmailView
                            , UserpasswordResetView
)
   






urlpatterns = [
    # path('account/',),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_efresh'),
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('login/', UserLoginview.as_view(), name='login_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('changepassword/', UserChangepasswordView.as_view(), name='chanage_password'),
    path('send-reset-password-email/', SendPasswordRestEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserpasswordResetView.as_view(), name='reset_password'),



]

