from django.urls import path
from .views import (
    UserProfileListCreateAPIView, 
    UserProfileRetrieveUpdateDestroyAPIView,
    PetListCreateAPIView,
    PetRetrieveUpdateDestroyAPIView,
    MatchCreateAPIView,
    MatchListAPIView,
    MessageListCreateAPIView
)

urlpatterns = [
    path('profiles/', 
         UserProfileListCreateAPIView.as_view(), 
         name='userprofile-list-create'),
         
    path('profiles/<int:pk>/', 
         UserProfileRetrieveUpdateDestroyAPIView.as_view(), 
         name='userprofile-detail'),
         
# API dla Pupili
    
    path('pets/', 
         PetListCreateAPIView.as_view(), 
         name='pet-list-create'),
         
    path('pets/<int:pk>/', 
         PetRetrieveUpdateDestroyAPIView.as_view(), 
         name='pet-detail'),
         
# API dla Matchy 
    
    path('matches/', 
         MatchListAPIView.as_view(), 
         name='match-list'),
         
    path('matches/like/', 
         MatchCreateAPIView.as_view(), 
         name='match-like'),
         
# API dla Wiadomości
    
    path('matches/<int:match_id>/messages/', 
         MessageListCreateAPIView.as_view(), 
         name='message-list-create'),
]