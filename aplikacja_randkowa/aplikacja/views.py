from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
import datetime
from .models import UserProfile

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
    return render(request, "aplikacja/osoba/list.html", {'users': uzytkownicy})

def user_detail_html(request, id):
    try:
        user_profile = UserProfile.objects.get(id=id)
    except UserProfile.DoesNotExist:
        raise Http404("Obiekt o podanym id nie istnieje")

    if request.method == "POST":
        user_profile.delete()
        return redirect('user_list_html')

    return render(request,
                  "aplikacja/osoba/detail.html",
                  {'user': user_profile})

def user_create_html(request):
    if request.method == "GET":
        return render(request, "aplikacja/osoba/create.html")
    
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        city = request.POST.get('city')
        bio = request.POST.get('bio')
        
        if first_name and city:
            try:
                UserProfile.objects.create(
                    user=request.user, 
                    first_name=first_name,
                    city=city,
                    bio=bio,
                )
                return redirect('user_list_html')
            except Exception as e:
                error = f"Błąd tworzenia: {e}"
                return render(request, "aplikacja/osoba/create.html", {'error': error})

        else:
            error = "Wszystkie pola są wymagane."
            return render(request, "aplikacja/osoba/create.html", {'error': error})
