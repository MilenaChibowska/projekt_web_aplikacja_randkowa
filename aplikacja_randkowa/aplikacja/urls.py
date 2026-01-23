from django.urls import path
# Importujemy funkcje bezpośrednio, tak jak miałaś to zaczęte
from .views import (
    welcome_view,
    user_list_html, # To jest Twoja funkcja od kart HTML
    UserProfileListCreateAPIView, 
    UserProfileRetrieveUpdateDestroyAPIView,
    PetListCreateAPIView,
    PetRetrieveUpdateDestroyAPIView,
    MatchCreateAPIView,
    MatchListAPIView,
    MessageListCreateAPIView
)

urlpatterns = [
    # Strona powitalna
    path('welcome/', welcome_view, name='welcome'),
    
    # TWOJA STRONA Z KARTAMI (wybieramy jeden stały adres)
    path('osoby-html/', user_list_html, name='user_list_html'),
    
    # API (reszta Twoich ścieżek)
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