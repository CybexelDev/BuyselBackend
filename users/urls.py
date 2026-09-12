from django.urls import path,re_path
from . import views
from developer.views import *
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from users.sitemaps import StaticViewSitemap


urlpatterns = [
    path('sitemap.xml',views.sitemap_view, name='sitemap'),
    path("about/", views.about, name="about"),
    path("", views.index, name="index"),
    path("base",views.base),
    path("blog/",views.blog,name="blog"),
    path("agent/",views.agents, name="agents"),
    path('agentform',views.agent_form, name="agent_form"),
    path('property', views.property_form, name='property_form'),
    path('faq', views.faq, name='faq'),
    path('more', views.more, name='more'),
    path('properties', views.properties, name='properties'),
    path("contact/", views.contact, name="contact"),
    path("agents/<int:pk>/", views.agent_detail, name="agent_detail"),
    path('property_detail/<int:pk>/', views.property_detail, name="property_detail"),
    path('agent_property_detail/<int:pk>/', views.agent_property_detail, name="agent_property_detail"),
    path('gallery/<int:pk>/', views.gallery, name="gallery"),
    path('agentgallery/<int:pk>/', views.property_gallery, name="property_gallery"),
    path("nearest_property/", views.nearest_property, name="nearest_property"),
    path("properties/", views.properties, name="properties"),
    path("filter-properties/", views.filter_properties, name="filter_properties"),
    path("upload-screenshot/", views.upload_property_screenshot, name="upload_property_screenshot"),
    path("upload-agent_screenshot/", views.upload_agents_screenshot, name="upload_agents_screenshot"),
    path('privacy', views.privacy, name="privacy"),
]
