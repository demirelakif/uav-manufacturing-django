from django.contrib import admin
from django.urls import path
from api.views import StaffApi,StaffAuthToken,RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/',StaffApi.as_view()),
    path('login/',StaffAuthToken.as_view()),
    path('register/', RegisterView.as_view()),
]
