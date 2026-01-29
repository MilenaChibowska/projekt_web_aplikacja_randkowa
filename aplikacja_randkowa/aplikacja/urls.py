from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
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

    path('api-auth/', include('rest_framework.urls')),
    
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]