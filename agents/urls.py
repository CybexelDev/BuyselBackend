from django.urls import path
from . import views
urlpatterns = [
    path('agentslogin/', views.premium_login, name='agentslogin'),
    # path('logout/', views.logout_view, name='logout'),

    
    # path('check-pin-code-messages/', views.check_pin_code_messages, name='check_pin_code_messages'),
    # path('remove-message/', views.remove_message, name='remove_message'),
    # path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),

    path('agent_dashboard', views.agents_dashboard, name='agent_dashboard'),
    path("change-password", views.change_password, name="change_password"),
    path('agent_add_property', views.agents_add_property, name='agent_add_property'),
    path('agent_add_property/edit/<int:property_id>/', views.agent_edit_property, name='agent_edit_property'),
    path('delete_property/<int:pk>/', views.agent_delete_property, name='agent_delete_property'),

    path("submit", views.submit, name="request"),
    path("contact-requests", views.contact_requests_list, name="contact_requests_list"),
    path("contact-requests/delete/<int:pk>/", views.delete_contact_request, name="delete_contact_request"),
    path('messages', views.agent_messages, name='agent_messages'),
    path('agent/messages/delete/<int:message_id>/', views.delete_inbox_message, name='delete_inbox_message'),

]

