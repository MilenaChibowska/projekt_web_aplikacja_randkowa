from django.urls import path
from . import views

urlpatterns = [
    path("welcome/", views.welcome_view, name="welcome"),
    
    path("html/osoby/", views.user_list_html, name="user_list_html"),
    
    path("html/osoby/<int:id>/", views.user_detail_html, name="user_detail"),
    
    path("html/osoby/dodaj/", views.user_create_html, name="user_create"),
]