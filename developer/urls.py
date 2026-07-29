from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('',views.admin_page,name='admin_panel'),
    path('base2', views.base, name="base2"),
    path('superuser-login/', views.superuser_login_view,name="superuser_login_view" ),
    # path('agenthouse/<uuid:pk>//edit/', views.agent_house_update, name='agenthouse-update'),
   

    # path('create/', views.create_blog, name='create_blog'),
    # path('update/<int:blog_id>/', views.update_blog, name='update_blog'),
    # path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
    # path('delete/inbox/<int:pk>/', views.inbox_delete, name='delete_inbox'),

    path('logout/', views.superuser_logout_view, name='superuser_logout'),
    path('logout/', views.superuser_logout_view, name='logout'),

    path('dashboard', views.Dashboard, name='dashboard'),
    path('category', views.categories, name="categories"),
    path('add_property', views.add_property, name="add_property"),
    path('add_property/edit/<uuid:property_id>/', views.edit_property, name='edit_property'),
    path('delete_property/<uuid:property_id>/', views.delete_property, name='delete_property'),
    path(
        "add_property/get/<uuid:property_id>/",
        views.get_property,
        name="get_property"
    ),
    path(
        'add_property/edit/<uuid:property_id>/',
        views.edit_property,
        name='edit_property'
    ),

    path(
        'delete_property/<uuid:property_id>/',
        views.delete_property,
        name='delete_property'
    ),

    # Ads Dashboard
    path(
        "ads/",
        views.ads_dashboard,
        name="ads_dashboard"
    ),

    # Banner
    path(
        "ads/banner/add/",
        views.add_banner,
        name="add_banner"
    ),

    path(
        "ads/banner/edit/<uuid:id>/",
        views.edit_banner,
        name="edit_banner"
    ),

    path(
        "ads/banner/delete/<uuid:id>/",
        views.delete_banner,
        name="delete_banner"
    ),

    # Slider

    path(
        "ads/slider/add/",
        views.add_slider,
        name="add_slider"
    ),

    path(
        "ads/slider/edit/<uuid:id>/",
        views.edit_slider,
        name="edit_slider"
    ),

    path(
        "ads/slider/delete/<uuid:id>/",
        views.delete_slider,
        name="delete_slider"
    ),

    # =====================================================
    # Dashboard
    # =====================================================

    path(
        "advertisement-notifications/",
        views.advertisement_notifications,
        name="advertisement_notifications"
    ),

    # =====================================================
    # Detail
    # =====================================================

    path(
        "advertisement-notifications/<str:request_type>/<uuid:id>/",
        views.notification_detail,
        name="notification_detail"
    ),

    # =====================================================
    # Mark Read
    # =====================================================

    path(
        "advertisement-notifications/<str:request_type>/<uuid:id>/mark-read/",
        views.mark_notification_read,
        name="mark_notification_read"
    ),

    # =====================================================
    # Update Status
    # =====================================================

    path(
        "advertisement-notifications/<str:request_type>/<uuid:id>/update-status/",
        views.update_status,
        name="update_status"
    ),

    path(
        "subscriptions/",
        views.subscription_dashboard,
        name="subscription_dashboard",
    ),



    # ==========================================
    # AGENT
    # ==========================================

    # path(
    #     "my-advertisement-requests/",
    #     views.my_advertisement_requests,
    #     name="my_advertisement_requests"
    # ),




    path('agents_login',views.agents_login, name="agents_login"),
    path('admin_premiumagents',views.admin_premiumagents, name="admin_premiumagents"),
    path('admin_premium/<int:pk>/', views.edit_premium, name="edit_premium"),
    path('admin_premium/delete/<int:pk>/', views.delete_premium, name="delete_premium"),
    path('admin_agents', views.admin_agents, name='admin_agents'),
    path('admin_agents/<int:pk>/', views.edit_agent, name="edit_agent"),
    path("agents/delete/<int:pk>/", views.delete_agent, name="delete_agent"),
    

    path(
        "blogs/",
        views.blog_dashboard,
        name="blog_dashboard"
    ),

    path(
        "blogs/edit/<uuid:id>/",
        views.edit_blog,
        name="edit_blog"
    ),

    path(
        "blogs/delete/<uuid:id>/",
        views.delete_blog,
        name="delete_blog"
    ),



    # path('admin_blogs', views.create_blog, name='create_blog'),
    # path('admin_blogs/<uuid:blog_id>/', views.update_blog, name='update_blog'),
    # path('admin_blogs/delete/<uuid:pk>/', views.delete_blog, name='delete_blog'),
    path('admin_contact', views.admin_contact, name="admin_contact"),
    path("contact/delete/<int:pk>/", views.delete_contact, name="delete_contact"),
    path('admin_message', views.admin_message, name="admin_message"),
    path("message/delete/<int:pk>/", views.delete_message, name="delete_message"),
    path('admin_agent_reg', views.admin_agent_reg, name="agent_reg"),
    path("delete_agent_reg/delete/<int:pk>/", views.delete_agent_reg, name="delete_agent_reg"),
    path('property_list', views.admin_property_list, name="admin_property_list"),
    path("property_list/delete/<int:pk>/", views.delete_property_list, name="delete_property_list"),
    path('admin_request', views.admin_request, name="requestforms"),
    path('admin_request/delete/<int:pk>/', views.delete_requestforms, name="admin_request"),
    path('expired_property', views.expired_property, name='expired_property'),
    path('expired_property/edit/<int:property_id>/', views.edit_exproperty, name="edit_exproperty"),
    path('delete_exproperty/<int:pk>/', views.expired_property_delete, name="expired_property_delete"),
    path('delete_premium_expire/<int:pk>/', views.delete_premium_expire, name="delete_premium_expire"),

    path('expired_agent', views.expire_premium, name='expired_agent'),
    path('delete_exagents/<int:pk>/', views.delete_agents_expire, name="delete_agents_expire"),

    path('admin_expirepremium/<int:pk>/', views.edit_expirepremium, name="edit_expirepremium"),
    path('admin_expireagent/<int:pk>/', views.edit_expireagent, name="edit_expireagent"),
    # path("register/", views.blog_register, name="blog_register"),
    # path("blogdashboard/", views.blog_dashboard, name="blog_dashboard"),
    # path("blogdashboard/create/", views.blog_dashboard_create, name="blog_dashboard_create"),
    # path("blogdashboard/update/<int:blog_id>/", views.blog_dashboard_update, name="blog_dashboard_update"),
    # path("blogdashboard/delete/<int:blog_id>/", views.blog_dashboard_delete, name="blog_dashboard_delete"),
    # path("bloglogin/", views.blog_login, name="blog_login"),
    # path("bloglogout/", views.blog_logout, name="blog_logout"),

    path("ajax/property-search/", views.property_live_search, name="property_live_search"),

    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('get-subcategory-fields/<int:subcategory_id>/', views.get_subcategory_fields, name='get_subcategory_fields'),

    path('get-user-details/<int:user_id>/', views.get_user_details, name='get_user_details'),

    path('useradd',views.AddUser, name='adduser'),
    path('plans',views.plans, name="userplan"),
    path('promotion',views.promotion, name='promotion'),
    path("export-users/", views.export_users_excel, name="export_users_excel"),

    path("agent_register/",views.agent_registration,name="agent_registration"),
    path('pending-agents/', views.pending_agents_list_view, name='pending_agents_list'),
    path('approve-agent/<uuid:agent_id>/', views.approve_agent, name='approve_agent'),
    path('reject-agent/<uuid:agent_id>/', views.reject_agent, name='reject_agent'),


path("testimonials/", views.testimonial_admin_view, name="testimonial"),
path("testimonials/delete/<int:id>/", views.delete_testimonial, name="delete_testimonial"),
path("edit-testimonial/<int:id>/", views.edit_testimonial, name="edit_testimonial"),
path("userprofiles/", views.userprofile_list_view, name="userprofiles"),
path("userprofiles/edit/<int:id>/", views.edit_userprofile, name="edit_userprofile"),
path("userprofiles/delete/<int:id>/", views.delete_userprofile, name="delete_userprofile"),
path("packages/", views.package_dashboard, name="package_dashboard"),
    # path("packages/delete/<str:type>/<int:id>/", views.delete_package, name="delete_package"),
    path(
    "packages/delete/<str:type>/<uuid:id>/",
    views.delete_package,
    name="delete_package"
),
    re_path(r'^.*$', views.superuser_login_view, name="redirect_to_index"),
    
]


    

   
    # path("banner-management/",views.slider_banner_view,name="slider_banner"),
    # path('hero-images/', views.hero_management, name='hero_management'),


