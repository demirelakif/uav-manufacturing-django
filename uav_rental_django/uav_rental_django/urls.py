from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StaffApi, StaffAuthToken, RegisterView, TeamViewSet, PartViewSet, AircraftViewSet,part_list,staff_list,aircraft_list
from uav_rental_django import views  # HTML view'larını dahil et

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')  # Team endpoint'i
router.register(r'parts', PartViewSet, basename='part')  # Part endpoint'i
router.register(r'aircrafts', AircraftViewSet, basename='aircraft')  # Aircraft endpoint'i

urlpatterns = [
    # Admin paneli
    path('admin/', admin.site.urls),

    # API endpoint'leri
    path('api/staff/', StaffApi.as_view()),  # API için staff endpoint'i
    path('api/login/', StaffAuthToken.as_view()),  # Login API endpoint'i
    path('api/register/', RegisterView.as_view()),  # Kayıt API endpoint'i
    path('api/', include(router.urls)),  # ViewSet API rotaları (teams, parts, aircrafts)

    # HTML View'ları
    path('dashboard/', views.dashboard, name='dashboard'),  # Kullanıcıya özel dashboard
    path('login/', views.login_view, name='login'),  # Login sayfası
    path('register/', views.register_view, name='register'),  # Kayıt sayfası
    path('logout/', views.logout_view, name='logout'),  # Logout sayfası
    path('parts/create/', views.part_create_view, name='part_create'),  # Parça 
    path('aircraft/create/', views.aircraft_create_view, name='aircraft_create'),  # Parça oluşturma sayfası
    path('api/parts_list/', part_list, name='part_list'),
    path('api/staff_list/', staff_list, name='staff_list'),
    path('api/aircraft_list/',aircraft_list, name='aircraft_list'),
    
]
