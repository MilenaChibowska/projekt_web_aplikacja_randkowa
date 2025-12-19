from django.urls import path
from .views import (
    welcome_view,
    user_list_html,
    
    UserProfileListCreateAPIView, 
    UserProfileRetrieveUpdateDestroyAPIView,
    PetListCreateAPIView,
    PetRetrieveUpdateDestroyAPIView,
    MatchCreateAPIView,
    MatchListAPIView,
    MessageListCreateAPIView
)

urlpatterns = [
    path('welcome/', welcome_view, name='welcome'),
    path('profiles-raw/', user_list_html, name='user-list-raw'),
    path('profiles-html/', user_list_html, name='user-list-html'),

    path('profiles/', 
         UserProfileListCreateAPIView.as_view(), 
         name='userprofile-list-create'),
         
    path('profiles/<int:pk>/', 
         UserProfileRetrieveUpdateDestroyAPIView.as_view(), 
         name='userprofile-detail'),
         
    path('pets/', 
         PetListCreateAPIView.as_view(), 
         name='pet-list-create'),
         
    path('pets/<int:pk>/', 
         PetRetrieveUpdateDestroyAPIView.as_view(), 
         name='pet-detail'),
         
    path('matches/', 
         MatchListAPIView.as_view(), 
         name='match-list'),
         
    path('matches/like/', 
         MatchCreateAPIView.as_view(), 
         name='match-like'),
         
    path('matches/<int:match_id>/messages/', 
         MessageListCreateAPIView.as_view(), 
         name='message-list-create'),
]