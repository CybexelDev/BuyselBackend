from django.urls import path
# from . views import *
from . import views
# from .views import save_screenshot

from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from users.sitemaps import StaticViewSitemap  # Replace with your actual import

sitemaps = {
    'static': StaticViewSitemap(),
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("",views.index, name="index"),
    path("base",views.base),
    path("blog",views.blog,name="blog"),
    # path('detail/<str:model_name>/<int:object_id>/', views.detail_view, name='detail_view'),
    path('detail<str:model_name>/<uuid:object_id>/', views.detail_view, name='detail_view'),
    
    path("agent/",views.agents, name="agents"),
    path('agents/<uuid:profile_id>/', views.agents_view, name='agents_view'),
    path('agents/detail/<str:model_name>/<uuid:object_id>/', views.agents_detail, name='agents_detail'), 
    # path('agent/<uuid:id>/', views.agents_view, name='agent_view'),   # Corrected parameter name
    # path('<str:model_name>/<uuid:id>/', views.agent_detail, name='agent_detail'),
    # path('agentdetail/<str:model_name>/<int:object_id>/', views.agent_detail_view, name='agent_detail_view'),
    path('agentform',views.agent_form, name="agent_form"),
    path('property', views.property_form, name='property_form'),
    path('faq', views.faq, name='faq'),
    path('more', views.more, name='more'),
    path('properties', views.properties, name='properties'),
    # path("share_property/", views.share_property, name="share_property"),
    # path("save-screenshot/", views.save_screenshot, name="save_screenshot"),
    # path("share-img/", views.shareimg, name="shareimg"),
    # path("save-screenshot/", save_screenshot, name="save_screenshot"),


    # path('message/', views.message_view, name='message_view'),
]
