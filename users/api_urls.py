from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("properties", PropertyViewSet, basename="properties")

urlpatterns = [

    # Property API
    path("property/", include(router.urls)),

    # Premium Login API
    # path("premium/login/", PremiumLoginAPIView.as_view(), name="premium_login"),

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

path("inbox/create/", InboxCreateAPIView.as_view(), name="inbox-create"),
path('agent/inbox/<uuid:agent_id>/', AgentInboxAPIView.as_view(), name='agent-inbox'),
path("message/remove/<int:message_id>/", RemoveMessageAPIView.as_view(), name="message-remove"),
path("inbox/list/", InboxListAPIView.as_view(), name="inbox-list"),
    path('agents/', AgentListAPIView.as_view(), name='agents-list'),
    path('agent/register/', AgentRegisterAPIView.as_view(), name='agent-register'),
    path('agent/login/', AgentLoginAPIView.as_view(), name='agent-login'),
    path('agent/profile/', AgentProfileAPIView.as_view(), name='agent-profile'),
    path("premium-plans/add/", PremiumPlanCreateAPIView.as_view(), name="premium-plan-add"),
    path("elite-plans/add/", ElitePlanCreateAPIView.as_view(), name="elite-plan-add"),
    path("premium-plans/", PremiumPlanListAPIView.as_view(), name="premium-plan-list"),
    path("elite-plans/", ElitePlanListAPIView.as_view(), name="elite-plan-list"),
    path("all-plans/", AllPlansAPIView.as_view(), name="all-plans"),

    



]