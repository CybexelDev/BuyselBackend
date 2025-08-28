from django.urls import path
from . import views
urlpatterns = [
    path('agentslogin/', views.agentslogin, name='agentslogin'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),

    # path('dashboard/houses', views.houses, name='houses'),
    # path('house/create/', views.house_create, name='house_create'),
    # path('house/update/<int:pk>/', views.house_update, name='house_update'),
    # path('house/delete/<int:pk>/', views.house_delete, name='house_delete'),
    # path('profile', views.profile_page, name='profile'),
    
    path('dashboard/profile', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('check-pin-code-messages/', views.check_pin_code_messages, name='check_pin_code_messages'),
    # path('remove-message/', views.remove_message, name='remove_message'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
]

