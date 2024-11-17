from rest_framework import serializers
from .models import Staff



class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['username','password']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['name', 'username', 'password']

    def create(self, validated_data):
        # Şifreyi hashleyerek kullanıcıyı oluşturuyoruz
        user = Staff(
            name=validated_data['name'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Şifre hashlenir
        user.save()
        return user
