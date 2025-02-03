from django.urls import path , include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from . import views
router = routers.DefaultRouter()

router.register(r"register", views.RegisterAPI, "register")
router.register(r"logout", views.LogoutView, "logout")


urlpatterns = [
      path("api/", include(router.urls)),
      path("api/login/", views.CustomAuthToken.as_view(), name="custom_api_token_auth"),
      path('api/account/change-password/', views.ChangePasswordAPI.as_view(), name='change-password'),
      path('api/reset-password-request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
      path('api/reset-password-confirm/<int:user_id>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


]

