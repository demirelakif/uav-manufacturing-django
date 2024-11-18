from rest_framework import serializers
from .models import Staff,Team, Part, Aircraft



class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'team']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())  # Team seçimi için ekleme

    class Meta:
        model = Staff
        fields = ['name', 'username', 'password', 'team']

    def create(self, validated_data):
        user = Staff(
            name=validated_data['name'],
            username=validated_data['username'],
            team=validated_data['team']  # Team bilgisini kaydet
        )
        user.set_password(validated_data['password'])  # Şifre hashlenir
        user.save()
        return user
    


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'part_type', 'team', 'stock', 'assigned_aircraft', 'part_aircraft']



class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'aircraft_type', 'produced_by', 'production_date']
