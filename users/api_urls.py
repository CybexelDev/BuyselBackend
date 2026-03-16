from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("properties", PropertyViewSet, basename="properties")

urlpatterns = [

    # Property API
    path("property/", include(router.urls)),

    # Premium Login API
    path("premium/login/", PremiumLoginAPIView.as_view(), name="premium_login"),

    path("request/create/", RequestCreateAPIView.as_view()),

    path("budget/", BudgetListAPIView.as_view()),

    path("category/", CategoryListView.as_view()),

    path("premium/change-password/", PremiumPasswordChangeAPIView.as_view()),

    # ✅ Featured Properties (PATH METHOD)
    path(
        "featured/",
        FeaturedPropertyViewSet.as_view({'get': 'list'}),
        name="featured-properties"
    ),
    path("agent/create/", AgentFormView.as_view(), name="agent-create"),
    path("user/register/", RegisterAPI.as_view()),
    path("user/verify-otp/", VerifyOTPAPI.as_view()),
    path("user/resent-otp/", ResendOTPAPI.as_view(), name="resend-otp"),

    path("user/forgot-password/",ForgotPasswordAPI.as_view()),

    path("user/verify-forgot-otp/",VerifyForgotOTPAPI.as_view()),

    path("user/change-password/",ChangePasswordAPI.as_view()),
    path("userlogin/", UserLoginAPI.as_view(), name="user-login"),

    path("profile/", UserProfileView.as_view()),
    path("profile/image/", UserProfileImageUpdateView.as_view()),
    path("profile/change-password/", UserChangePasswordView.as_view()),

    path("amenities/", AmenitiesListCreateView.as_view()),
    path("refresh/", RefreshTokenView.as_view()),


]