from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StaffApi, StaffAuthToken, RegisterView, TeamViewSet, PartViewSet, AircraftViewSet,part_list,staff_list,aircraft_list
from uav_manufacturing_django import views  # HTML view'larını dahil et
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Dokümantasyonu",
        default_version='v1',
        description="Hava Aracı Üretim Uygulaması.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="demirel.akif@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team') 
router.register(r'parts', PartViewSet, basename='part') 
router.register(r'aircrafts', AircraftViewSet, basename='aircraft')  
urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', views.dashboard, name='dashboard'),  # Kullanıcıya özel dashboard
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_view, name='register'),  
    path('logout/', views.logout_view, name='logout'),  

    path('parts/create/', views.part_create_view, name='part_create'), 
    path('aircraft/create/', views.aircraft_create_view, name='aircraft_create'), 
    # API endpoint'leri
    path('api/parts_list/', part_list, name='part_list'),
    path('api/staff_list/', staff_list, name='staff_list'),
    path('api/aircraft_list/',aircraft_list, name='aircraft_list'),
    path('parts/delete/<int:id>/', views.part_delete_view, name='part_delete'),
    path('api/staff/', StaffApi.as_view()),  # API için staff endpoint'i
    path('api/login/', StaffAuthToken.as_view()),  # Login API endpoint'i
    path('api/register/', RegisterView.as_view()),  # Kayıt API endpoint'i
    path('api/', include(router.urls)),  # ViewSet API rotaları (teams, parts, aircrafts)

    #swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
