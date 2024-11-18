from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StaffSerializer, RegisterSerializer
from .models import Staff
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Team, Part, Aircraft
from .serializers import TeamSerializer, PartSerializer, AircraftSerializer
from django.shortcuts import get_object_or_404


class StaffApi(APIView): 
    permission_classes = [IsAuthenticated]  # only authenticated users can access this view
    def get(self, request):
        queryset = Staff.objects.all()
        serializer = StaffSerializer(queryset,many=True)
        return Response({
            "status": True,
            "data": serializer.data
        })



class StaffAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise AuthenticationFailed("Invalid credentials or inactive account")

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username, 'name': user.name})


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "team": user.team.name
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    






# Takım bilgilerini listelemek için
class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        # Kullanıcının takımına göre parçaları filtrele
        user_team = self.request.user.team
        return Part.objects.filter(team=user_team)

    def create(self, request, *args, **kwargs):
        # Kullanıcının takımını al
        team_id = request.user.team.id

        # `request.data`'ya takım bilgisini ekle
        mutable_data = request.data.copy()  # `request.data` immutable olduğundan kopyalıyoruz
        mutable_data['team'] = team_id


        # Yeni `request` objesi oluştur ve `data`yı güncelle
        request._full_data = mutable_data

        # Part kontrolünü burada yapabilirsiniz
        part_type = mutable_data.get('part_type')
        allowed_parts = {
            'kanat': 'kanat_takim',
            'govde': 'govde_takim',
            'kuyruk': 'kuyruk_takim',
            'aviyonik': 'aviyonik_takim',
        }

        if allowed_parts.get(part_type) != request.user.team.name:
            return Response({"error": "Bu takım bu tür bir parça üretemez!"}, status=400)

        return super().create(request, *args, **kwargs)
    

    def destroy(self, request, *args, **kwargs):
        # Parçayı almak
        part = self.get_object()

        # Eğer parça, kullanıcının takımıyla eşleşmiyorsa silmeye izin verme
        if part.team != request.user.team:
            return Response({"error": "Sadece kendi takımınıza ait parçaları silebilirsiniz!"}, status=400)

        # Silme işlemi
        return super().destroy(request, *args, **kwargs)



# Uçak işlemleri için
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        aircraft_type = request.data.get('aircraft_type')
        required_parts = {
            'tb2': ['kanat', 'govde', 'kuyruk', 'aviyonik'],
            'tb3': ['kanat', 'govde', 'kuyruk', 'aviyonik'],
            'akinci': ['kanat', 'govde', 'kuyruk', 'aviyonik'],
            'kizilelma': ['kanat', 'govde', 'kuyruk', 'aviyonik'],
        }

        missing_parts = []
        for part in required_parts.get(aircraft_type, []):
            if not Part.objects.filter(part_type=part, stock__gt=0).exists():
                missing_parts.append(part)

        if missing_parts:
            return Response({"error": f"Eksik parçalar: {', '.join(missing_parts)}"}, status=400)

        for part_type in required_parts[aircraft_type]:
            part = Part.objects.filter(part_type=part_type, stock__gt=0).first()
            part.stock -= 1
            part.save()

        return super().create(request, *args, **kwargs)