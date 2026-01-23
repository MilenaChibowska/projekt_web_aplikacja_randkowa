from django.shortcuts import render


from django.http import HttpResponse 
import datetime
from django.db.models import Q
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserProfile, Pet, Match, Message
from .serializers import (
    UserProfileSerializer, 
    PetSerializer, 
    MatchSerializer, 
    MessageSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)

def user_list_html(request):
    uzytkownicy = UserProfile.objects.all()
    return HttpResponse(uzytkownicy)

def user_list_template(request):
    uzytkownicy = UserProfile.objects.all()
    return render(request, 'osoby_lista.html', {'users': uzytkownicy})

#  Widoki dla UserProfile

class UserProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

# Szczegóły profilu

class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

# Widoki dla Pet

class PetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

class PetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

# Widoki dla Match

class MatchCreateAPIView(generics.CreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

# Listowanie Matchy

class MatchListAPIView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        
        return Match.objects.filter(
            Q(swiper=user_profile) | Q(target=user_profile)
        ).select_related('swiper', 'target')
    
# Widok dla modelu Message

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ID Match, które przekazujemy w adresie URL
        match_id = self.kwargs['match_id'] 
        
        # Sprawdzamy, czy zalogowany użytkownik jest stroną tego Match
        match = get_object_or_404(Match, pk=match_id)
        
        
        return Message.objects.filter(match_id=match_id).order_by('timestamp')

    def perform_create(self, serializer):
        match_id = self.kwargs['match_id']
        match_instance = get_object_or_404(Match, pk=match_id)
        
        serializer.save(match=match_instance)
