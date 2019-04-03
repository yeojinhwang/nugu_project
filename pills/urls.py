from django.urls import path
from . import views


urlpatterns = [
    path('health', views.health, name='health'),
    path('request_pills', views.request_pills, name='request_pills'),
    path('request_pills_pregnant', views.request_pills_pregnant, name='request_pills_pregnant'),
    path('request_pills_oldman', views.request_pills_oldman, name='request_pills_oldman'),
    path('request_pills_interaction', views.request_pills_interaction, name='request_pills_interaction')
]