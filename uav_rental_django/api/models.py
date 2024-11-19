from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

AIRCRAFT_TYPES = [
        ('tb2', 'TB2'),
        ('tb3', 'TB3'),
        ('akinci', 'AKINCI'),
        ('kizilelma', 'KIZILELMA'),
    ]

class Team(models.Model):
    TEAM_TYPES = [
        ('kanat_takim', 'Kanat Takımı'),
        ('govde_takim', 'Gövde Takımı'),
        ('kuyruk_takim', 'Kuyruk Takımı'),
        ('aviyonik_takim', 'Aviyonik Takımı'),
        ('montaj_takim', 'Montaj Takımı'),
    ]
    name = models.CharField(max_length=50, choices=TEAM_TYPES, unique=True)

    def __str__(self):
        return self.name

class StaffManager(BaseUserManager):
    def create_user(self, username, password=None, name=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, name, **extra_fields)

class Staff(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # AbstractBaseUser'da zaten var
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')

    objects = StaffManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username


class Part(models.Model):
    PART_TYPES = [
        ('kanat', 'Kanat'),
        ('govde', 'Gövde'),
        ('kuyruk', 'Kuyruk'),
        ('aviyonik', 'Aviyonik'),
    ]

    part_type = models.CharField(max_length=50, choices=PART_TYPES)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='parts')
    part_aircraft = models.CharField(max_length=50, choices=AIRCRAFT_TYPES)
    stock = models.PositiveIntegerField(default=0)
    assigned_aircraft = models.ForeignKey('Aircraft', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.part_type} - {self.team.name} - Stock: {self.stock}"
    

class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=50, choices=AIRCRAFT_TYPES)
    # produced_by = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='aircrafts')
    production_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.aircraft_type} - {self.production_date}"