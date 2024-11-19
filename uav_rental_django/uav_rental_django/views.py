from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from api.models import Part, Team, Staff
from django.contrib.auth.decorators import login_required
from rest_framework.test import APIRequestFactory
from api.views import PartViewSet, AircraftViewSet
from django.contrib.auth import logout
from django.contrib import messages
from rest_framework.authtoken.models import Token

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # Başarılı girişte dashboard yönlendirme
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        team_id = request.POST.get("team")  # Kullanıcı seçilen takım

        # Kullanıcıyı oluştur
        user = Staff.objects.create_user(
            username=username, password=password, name=name, team_id=team_id
        )
        return redirect('login')  # Başarılı kayıt sonrası login ekranına yönlendirme

    teams = Team.objects.all()  # Takım listesini kayıtta sun
    return render(request, "register.html", {"teams": teams})



@login_required
def dashboard(request):
    # Oturum açmış kullanıcının takımına ait parçaları getir
    user_team = request.user.team
    parts = Part.objects.filter(team=user_team.id)
    staff_list = Staff.objects.filter(team=user_team)  # Tüm personelleri listele
    return render(request, "dashboard.html", {"parts": parts, "team": user_team,'staff_list': staff_list})




def logout_view(request):
    logout(request)
    return redirect('login')  # Login sayfasına yönlendir


@login_required
def aircraft_create_view(request):
    if request.method == 'POST':
        token = Token.objects.get(user=request.user)
        aircraft_type = request.POST.get('aircraft_type')
        # Sahte bir API isteği oluştur
        factory = APIRequestFactory()
        
        print("Auth Token User:")
        print(request.user) 
        # Kullanıcının token'ını almak
        token = request.user.auth_token.key if request.user.auth_token else None

        # Eğer token varsa, Authorization başlığını ekleyin
        api_request = factory.post('/api/aircrafts/', {
            'aircraft_type': aircraft_type,

        })

        if token:
            api_request.META['HTTP_AUTHORIZATION'] = f'token {token}'  # Token'ı ekle

        # Kullanıcıyı isteğe ekle
        api_request.user = request.user

        # PartViewSet'in create metodunu çağır
        view = AircraftViewSet.as_view({'post': 'create'})
        response = view(api_request)

        # Başarı durumunda dashboard'a yönlendir
        if response.status_code == 201:
            try :
                messages.success(request, response.data['message'])
            except:
                messages.success(request, "Successfully Produced")
        else:
            # Hata mesajını al ve kullanıcıya göster
            error_message = response.data.get('error', 'Bir hata oluştu!')
            messages.error(request, error_message)
            return redirect('aircraft_create')

    return render(request, 'aircraft_create.html')
    


@login_required
def part_create_view(request):
    if request.method == 'POST':
        print("Auth Token User:")
        print(request.user)
        part_type = request.POST.get('part_type')
        part_aircraft = request.POST.get('part_aircraft')  # Yeni eklenen uçak tipi
        stock = request.POST.get('stock')  # Yeni eklenen stok miktarı

        # Sahte bir API isteği oluştur
        factory = APIRequestFactory()
        
        # Kullanıcının token'ını almak
        token = request.user.auth_token.key if request.user.auth_token else None

        # Eğer token varsa, Authorization başlığını ekleyin
        api_request = factory.post('/api/parts/', {
            'part_type': part_type,
            'part_aircraft': part_aircraft,
            'stock': int(stock)  # Stock bilgisi
        })

        if token:
            api_request.META['HTTP_AUTHORIZATION'] = f'token {token}'  # Token'ı ekle

        print(token)
        # Kullanıcıyı isteğe ekle
        api_request.user = request.user

        # PartViewSet'in create metodunu çağır
        view = PartViewSet.as_view({'post': 'create'})
        response = view(api_request)

        # Başarı durumunda dashboard'a yönlendir
        if response.status_code == 201:
            try :
                messages.success(request, response.data['message'])
            except:
                messages.success(request, "Successfully Produced")
        else:
            # Hata mesajını al ve kullanıcıya göster
            error_message = response.data.get('error', 'Bir hata oluştu!')
            messages.error(request, error_message)
            return redirect('part_create')

    return render(request, 'part_create.html')