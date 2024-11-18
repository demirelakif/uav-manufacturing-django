from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import StaffApi,StaffAuthToken,RegisterView,TeamViewSet, PartViewSet,AircraftViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')  # Team endpoint'i
router.register(r'parts', PartViewSet, basename='part')  # Part endpoint'i
router.register(r'aircrafts', AircraftViewSet, basename='aircraft')  # Aircraft endpoint'i


urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/',StaffApi.as_view()),
    path('login/',StaffAuthToken.as_view()),
    path('register/', RegisterView.as_view()),
    path('', include(router.urls)),  # ViewSet rotalarını ekle
    
]
