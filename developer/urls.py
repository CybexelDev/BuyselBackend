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
    path('add_property/edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('delete_property/<int:pk>/', views.delete_property, name='delete_property'),
    path('agents_login',views.agents_login, name="agents_login"),
    path('admin_premiumagents',views.admin_premiumagents, name="admin_premiumagents"),
    path('admin_premium/<int:pk>/', views.edit_premium, name="edit_premium"),
    path('admin_premium/delete/<int:pk>/', views.delete_premium, name="delete_premium"),
    path('admin_agents', views.admin_agents, name='admin_agents'),
    path('admin_agents/<int:pk>/', views.edit_agent, name="edit_agent"),
    path("agents/delete/<int:pk>/", views.delete_agent, name="delete_agent"),

    path('admin_blogs', views.create_blog, name='create_blog'),
    path('admin_blogs/<int:blog_id>/', views.update_blog, name='update_blog'),
    path('admin_blogs/delete/<int:pk>/', views.delete_blog, name='delete_blog'),
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
    re_path(r'^.*$', views.superuser_login_view, name="redirect_to_index"),

]