from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from agents.views import PlanListAPIView


# from django.urls import path
from .views import PropertyDetailAPIView
from django.urls import path
from .views import PropertyEnquiryListCreateView
from .views import RelatedPropertiesAPIView



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

    path("properties/", PropertyListAPI.as_view(), name="property-list"),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),


    path("amenities/", AmenitiesListCreateView.as_view()),
    path("refresh/", RefreshTokenView.as_view()),

    path('agent/inbox-message/', InboxCreateAPIView.as_view(), name='inbox-message'),
    path('agent/inbox-messages/', InboxListAPIView.as_view(), name='inbox-messages'),
    path('agent/inbox-message-delete/<int:id>/', InboxDeleteAPIView.as_view(), name='inbox-message-delete'),
    
    path('agents/', AgentListAPIView.as_view(), name='agents-list'),
    path('agent/register/', AgentRegisterAPIView.as_view(), name='agent-register'),
    path('agent/login/', AgentLoginAPIView.as_view(), name='agent-login'),
    path("agent/refresh-token/", AgentTokenRefreshAPIView.as_view(), name="agent-refresh-token"),
    path('agent/profile/', AgentProfileAPIView.as_view(), name='agent-profile'),
    path('agent/<str:agent_code>/contact/', AgentContactCreateAPIView.as_view()),
    path('agent/contacts/', AgentContactListAPIView.as_view()),
    path('agent/contact-delete/<int:id>/', AgentContactDeleteAPIView.as_view(), name='agent-contact-delete'),
    path('agent/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('agent/property/', AgentPropertyAPIView.as_view(), name='agent-property'),

    # Agent properties list
    path('agent/property/list/', AgentPropertyListAPIView.as_view(), name='agent-property-list'),

    # Single property detail
    path('agent/property/<int:id>/', AgentPropertyDetailAPIView.as_view(), name='agent-property-detail'),


    path('agent/plans/', PlanListAPIView.as_view(), name='plans-list'),

    path("property/<str:hash_id>/",PropertyDetailAPIView.as_view(),name="property-detail"),
    path('enquiries/', PropertyEnquiryListCreateView.as_view(), name='enquiry-list-create'),
    path("property/<str:hash_id>/related/",RelatedPropertiesAPIView.as_view(),name="related-properties"),
    path("contact/",ContactCreateAPIView.as_view(),name="contact-create"),


]