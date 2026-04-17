from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from agents.views import PlanListAPIView


# from django.urls import path
from .views import PropertyDetailAPIView
from django.urls import path
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
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path('agent/inbox-message/', InboxCreateAPIView.as_view(), name='inbox-message'),
    path('agent/inbox-messages/', InboxListAPIView.as_view(), name='inbox-messages'),
    path('agent/inbox-message-delete/<int:id>/', InboxDeleteAPIView.as_view(), name='inbox-message-delete'),
    path("agents/", AgentListAPIView.as_view(), name="agents-list"),
    path("agents/listing/", AgentListFrontendAPIView.as_view(), name="agents-frontend-list"),
    # path("agents/<str:agent_id>/reviews/submit/", SubmitAgentReviewAPIView.as_view()),
    path("agents/reviews/submit/<str:agent_id>/", SubmitAgentReviewAPIView.as_view()),
    # path("agents/<str:agent_id>/reviews/", AgentReviewListAPIView.as_view(), name="agent-review-list"), 
    path("agents/reviews/<str:agent_id>/", AgentReviewListAPIView.as_view(), name="agent-review-list"),
    
    path("reviews/like/<uuid:review_id>/", ToggleReviewLikeAPIView.as_view(), name="review-like"),
    # path("reviews/<uuid:review_id>/like/", ToggleReviewLikeAPIView.as_view(),name="review-like"),   # path('agent/register/', AgentRegisterAPIView.as_view(), name='agent-register'),
    path('agent/login/', AgentLoginAPIView.as_view(), name='agent-login'),
    path("agent/refresh-token/", AgentTokenRefreshAPIView.as_view(), name="agent-refresh-token"),
    path('agent/profile/', AgentProfileAPIView.as_view(), name='agent-profile'),
    path('agent/<str:agent_code>/contact/', AgentContactCreateAPIView.as_view()),
    path('agent/contacts/', AgentContactListAPIView.as_view()),
    path('agent/contact-delete/<int:id>/', AgentContactDeleteAPIView.as_view(), name='agent-contact-delete'),
    path('agent/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('agent/register-request/', AgentPendingRegisterAPIView.as_view(), name='api-pending-register'),
    path('agent/categories/', CategoryListAPIView.as_view(), name='agent_categories'),
    path('agent/subcategories/', SubcategoryListAPIView.as_view(), name='agent_subcategories'),
    path('agent/subcategory-fields/', SubcategoryFieldListAPIView.as_view(), name='agent_subcategory_fields'),
    path('agent/amenities/', AmenitiesAPIView.as_view(), name='agent_amenities'),
    path('agent/purposes/', PurposeListAPIView.as_view(), name='purpose_list'),

    path('agent/property-meta/', PropertyMetaAPIView.as_view(), name='property-meta'),
    
    # Agent properties list
    path('agent/property/', AgentPropertyAPIView.as_view(), name='agent-property'),

    path('agent/property/list/', AgentPropertyListAPIView.as_view(), name='agent-property-list'),
    path('agent/property-limits/', AgentPropertyLimitAPIView.as_view(), name='agent-property-limit'),

    # Single property detail
    path('agent/property/<int:id>/', AgentPropertyDetailAPIView.as_view(), name='agent-property-detail'),


    path('agent/plans/', PlanListAPIView.as_view(), name='plans-list'),
    path('agent/combined-data/', AgentPlanCombinedAPIView.as_view(), name='combined-data'),

    path("property/<str:hash_id>/",PropertyDetailAPIView.as_view(),name="property-detail"),
    path('enquiries/',PropertyEnquiryCreateView.as_view(), name='enquiry-list-create'),
    # path("property/<str:hash_id>/related/",RelatedPropertiesAPIView.as_view(),name="related-properties"),
    path("property/related/<str:hash_id>/", RelatedPropertiesAPIView.as_view(), name="related-properties"),
    path("contact/",ContactCreateAPIView.as_view(),name="contact-create"),
    path("blogs/", BlogListingAPIView.as_view(), name="blog-list"),
    path("blogs/<int:id>/", SingleBlogAPIView.as_view(), name="single-blog"),
    path("blogs/by-category/", BlogByCategoryAPIView.as_view()),
    path("blogs/search/", BlogNameSearchAPIView.as_view(), name="blog-search"),
    path("wishlist/clear/",BulkWishlistDeleteAPIView.as_view(),name="bulk-wishlist-delete"),
    path("wishlist/filter/",WishlistFilterAPIView.as_view()),
    path("wishlist/sort/", WishlistSortingAPIView.as_view()),
   
    path("profile/update/",UserProfileUpdateView.as_view(),name="profile-update"),

    path("my-activity/", MyActivityView.as_view(), name="my-activity"),
    # path("reviews/<uuid:review_id>/update/", UpdateAgentReviewAPIView.as_view()),
    # path("reviews/<uuid:review_id>/delete/", DeleteAgentReviewAPIView.as_view()),
    path("reviews/update/<uuid:review_id>/", UpdateAgentReviewAPIView.as_view()),
    path("reviews/delete/<uuid:review_id>/", DeleteAgentReviewAPIView.as_view()),
    path("sliderads/", ActiveSliderAdsAPIView.as_view(), name='slider_banners_api'),
    path("bannerads/", BannerAdsAPIView.as_view(), name='header_ads_api'),
    path("agent/detail/<str:agent_id>/", AgentDetailAPIView.as_view(), name='agent_detail'),
    path("properties/filter/", PropertyFilterAPIView.as_view()),

    # path("auth/facebook/login/", FacebookLoginRedirectView.as_view()),
    # path("auth/facebook/callback/", FacebookCallbackAPIView.as_view()),
    # path("data-deletion/", data_deletion),


]