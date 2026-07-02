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

    path('google-login/', GoogleLoginView.as_view(), name='google_login'),

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
    path("user/resent-forgot-otp/",ForgotPasswordResendOTPAPI.as_view()),
    path("user/verify-forgot-otp/",VerifyForgotOTPAPI.as_view()),

    path("user/change-password/",UserChangePasswordAPI.as_view()),
    path("userlogin/", UserLoginAPI.as_view(), name="user-login"),
    path("auth/facebook/login/", FacebookLoginAPI.as_view()),

    path("profile/", UserProfileView.as_view()),
    path("profile/image/", UserProfileImageUpdateView.as_view()),
    path("profile/change-password/", UserChangePasswordView.as_view()),

    path("properties/", PropertyListAPI.as_view(), name="property-list"),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),


    path("amenities/", AmenitiesListCreateView.as_view()),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path('agent/inbox-message/', InboxCreateAPIView.as_view(), name='inbox-message'),
    path('agent/inbox-messages/', InboxListAPIView.as_view(), name='inbox-messages'),
    path('agent/inbox-message-delete/<uuid:id>/', InboxDeleteAPIView.as_view(), name='inbox-message-delete'),
    path("agents/", AgentListAPIView.as_view(), name="agents-list"),
    path("agents/listing/", AgentListFrontendAPIView.as_view(), name="agents-frontend-list"),
    # path("agents/<str:agent_id>/reviews/submit/", SubmitAgentReviewAPIView.as_view()),
    path("agents/reviews/submit/<str:agent_id>/", SubmitAgentReviewAPIView.as_view()),
    # path("agents/<str:agent_id>/reviews/", AgentReviewListAPIView.as_view(), name="agent-review-list"), 
    path("agents/reviews/<str:agent_id>/", AgentReviewListAPIView.as_view(), name="agent-review-list"),
    
    path("reviews/like/<uuid:review_id>/", ToggleReviewLikeAPIView.as_view(), name="review-like"),
    # path("reviews/<uuid:review_id>/like/", ToggleReviewLikeAPIView.as_view(),name="review-like"),   # path('agent/register/', AgentRegisterAPIView.as_view(), name='agent-register'),
    path('agent/login/', AgentLoginAPIView.as_view(), name='agent-login'),
    path("agent/forgot-password/", AgentForgotPasswordAPI.as_view()),
    path("agent/resent-forgot-otp/",AgentResendForgotOTP.as_view()),
    path("agent/verify-forgot-otp/", AgentVerifyForgotOTP.as_view()),
    path("agent/change-password/", AgentChangePasswordAPI.as_view()),
    path("agent/refresh-token/", AgentTokenRefreshAPIView.as_view(), name="agent-refresh-token"),
    path('agent/profile/', AgentProfileAPIView.as_view(), name='agent-profile'),
    path('agent/profile-frontend/<str:agent_code>/', PublicAgentProfileAPIView.as_view(), name='public-agent-profile'),
    path('agent/contact/<uuid:agent_id>/', AgentContactCreateAPIView.as_view()),
    path('agent/contacts/', AgentContactListAPIView.as_view()),
    path('agent/contact-delete/<uuid:id>/', AgentContactDeleteAPIView.as_view(), name='agent-contact-delete'),
    path('agent/change_password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('agent/register-request/', AgentPendingRegisterAPIView.as_view(), name='api-pending-register'),
    path('agent/categories/', CategoryListAPIView.as_view(), name='agent_categories'),
    path('agent/subcategories/', SubcategoryListAPIView.as_view(), name='agent_subcategories'),
    path('agent/subcategory-fields/', SubcategoryFieldListAPIView.as_view(), name='agent_subcategory_fields'),
    path('agent/amenities/', AmenitiesAPIView.as_view(), name='agent_amenities'),
    path('agent/purposes/', PurposeListAPIView.as_view(), name='purpose_list'),
    path("agent_properties/enquiry/<int:id>/", AgentPropertyEnquiryCreateAPI.as_view(), name="property-enquiry"),
    path("agent/enquiries/", AgentPropertyEnquiryListAPI.as_view(), name="agent-enquiry-list"),
    path("agent/enquiry/<int:id>/",AgentPropertyEnquiryDetailAPI.as_view(),name="agent-enquiry-detail"),
    path("agent/dashboard/", DashboardAPIView.as_view(), name="agent-dashboard"),
    path('agent/property-meta/', PropertyMetaAPIView.as_view(), name='property-meta'),
    path("agent/contact-message/",AgentContactMessageCreateAPIView.as_view()),
    
    # Agent properties list
    path('agent/property/', AgentPropertyAPIView.as_view(), name='agent-property'),

    path('agent/property/list/', AgentPropertyListAPIView.as_view(), name='agent-property-list'),
    path('agent/property-limits/', AgentPropertyLimitAPIView.as_view(), name='agent-property-limit'),

    # Single property detail
    path('agent/property/<uuid:id>/', AgentPropertyDetailAPIView.as_view(), name='agent-property-detail'),
    path("user/property/<uuid:id>/", UserPropertyDetailAPIView.as_view()),
    # ✅ PUBLIC APIs (NO LOGIN)
    path('agent_properties/', PublicPropertyListAPIView.as_view(), name='public-property-list'),
    path('agent_properties/<uuid:uuid>/', PublicPropertyDetailAPIView.as_view(), name='public-property-detail'),


    path("agent/notifications/", AgentNotificationListAPI.as_view(), name="agent-notifications"),
    path("agent/notifications/read/<uuid:id>/", MarkNotificationReadAPI.as_view(), name="mark-notification-read"),
    path("agent/notifications/unread-count/", UnreadNotificationCountAPI.as_view(), name="unread-count"),

    path("agent/upgrade-plan/", AgentUpgradePlanAPIView.as_view(), name="upgrade-plan"),

    # path('agent/plans/', PlanListAPIView.as_view(), name='plans-list'),
    path('agent/current/plans/', PlanListAPIView.as_view(), name='current-subscription'),
    path('plans/normal/', AgentPlanListAPIView.as_view(), name='plans-normal'),
    path('plans/premium/', PremiumPlanListAPIView.as_view(), name='plans-premium'),
    path('plans/elite/', ElitePlanListAPIView.as_view(), name='plans-elite'),
    path('plans/all/', AllPlansAPIView.as_view(), name='plans-all'),
    path("agent-plans/",AgentPlansAPIView.as_view(),name="agent-plans"),
    path('agent/combined-data/', AgentPlanCombinedAPIView.as_view(), name='combined-data'),


    path("testimonial/list/", TestimonialListAPI.as_view(),name='testimonial-list'),
    path("property/<uuid:uuid>/",PropertyDetailAPIView.as_view(),name="property-detail"),
    # path('enquiries/',PropertyEnquiryCreateView.as_view(), name='enquiry-list-create'),
    # path("property/<str:hash_id>/related/",RelatedPropertiesAPIView.as_view(),name="related-properties"),
    path("property/related/<uuid:uuid_id>/", RelatedPropertiesAPIView.as_view(), name="related-properties"),
    path("contact/",ContactCreateAPIView.as_view(),name="contact-create"),
    path("blogs/", BlogListingAPIView.as_view(), name="blog-list"),
    path("blogs/<uuid:id>/", SingleBlogAPIView.as_view(), name="single-blog"),
    path("blogs/by-category/", BlogByCategoryAPIView.as_view()),
    path("blogs/search/", BlogNameSearchAPIView.as_view(), name="blog-search"),
    path("wishlist/clear/",BulkWishlistDeleteAPIView.as_view(),name="bulk-wishlist-delete"),
    path("wishlist/filter/",WishlistFilterAPIView.as_view()),
    path("wishlist/sort/", WishlistSortingAPIView.as_view()),
   
    path("profile/update/",UserProfileUpdateView.as_view(),name="profile-update"),

    path("my-activity/", MyActivityView.as_view(), name="my-activity"),
    path("reviews/update/<uuid:review_id>/", UpdateAgentReviewAPIView.as_view()),
    path("reviews/delete/<uuid:review_id>/", DeleteAgentReviewAPIView.as_view()),
    path("sliderads/", ActiveSliderAdsAPIView.as_view(), name='slider_banners_api'),
    path("bannerads/", BannerAdsAPIView.as_view(), name='header_ads_api'),
    path("agent/detail/<str:agent_id>/", AgentDetailAPIView.as_view(), name='agent_detail'),
    path("properties/filter/", PropertyFilterAPIView.as_view()),
    path("properties/search/", PropertySearchAPIView.as_view(), name="public-property-search"),
    path("property_enquiries/", PropertyEnquiryByUserAPIView.as_view()),

    path("nearby-properties/", NearbyPropertyAPIView.as_view(), name="nearby-properties"),
    path("agents/search/", AgentSearchAPIView.as_view(), name="agent-search"),
    path("agents/cities/", AgentCityListAPIView.as_view(), name="agent-cities"),
    path("enquiry/<int:enquiry_id>/", EnquiryDetailAPIView.as_view(), name="enquiry-detail"),
    path("properties/filters/", PropertyFilterOptionsAPIView.as_view(), name="property-filters"),
    path("citydistrict/filter/", CityDistrictFilterAPIView.as_view()),
    path("recent_enquiries/", RecentEnquiryAPIView.as_view()),
    path("agent-property-location/<str:agent_id>/",AgentPropertyLocationAPIView.as_view()),
    path("agent/property_cities/<str:agent_id>/",AgentPropertyCityFilterAPIView.as_view(),name="agent_property_cities"),
    path("agent/property-search/<str:agent_id>/",AgentPropertySearchAPIView.as_view(),name="agent_property_search"),
    path("all-properties/",CombinedPropertyListAPIView.as_view(),name="combined-property-list"),
    path("property-detail/<uuid:uuid_id>/",UniversalPropertyDetailAPIView.as_view(),name="property-detail"),
    path("enquiries/",UniversalPropertyEnquiryAPI.as_view(),name="property-enquiry"),
    path("enquiry/",UnifiedEnquiryListAPIView.as_view(),name="unified-enquiries"),
    path("filter/nearby-properties/",NearbyPropertyAPIView.as_view()),
    path("property-filter/",PropertiesFilterAPIView.as_view(),name="property-filter"),
    path("enquiry-detail/<uuid:enquiry_id>/",EnquiryDetailAPIView.as_view(),name="enquiry-detail"),


    path("activate-userplan/",ActivateUserPlanAPIView.as_view(),name="activate_user_plan"),
    path("current-userplan/",CurrentUserPlanAPIView.as_view(),name="current_userplan"),
    path("owner-dashboard/",OwnerDashboardAPIView.as_view(),name="owner-dashboard"),
    path("owner/property/list/",UserPropertyListAPIView.as_view(),name="user-properety-list"),
    path("owner/property/",UserPropertyCreateAPIView.as_view(),name="user-property-create"),


    path("create-payment/",CreatePaymentAPIView.as_view(),name="create_payment"),

    path("verify-payment/",VerifyPaymentAPIView.as_view(),name="verify_payment"),
    path("agent/advertisement-request/",AdvertisementRequestAPIView.as_view(),name="advertisement-request"),
    # path(
    #     "properties/",
    #     PublicPropertyListAPIView.as_view(),
    #     name="public-properties"
    # ),

    # path("auth/facebook/login/", FacebookLoginRedirectView.as_view()),
    # path("auth/facebook/callback/", FacebookCallbackAPIView.as_view()),
    # path("data-deletion/", data_deletion),


]