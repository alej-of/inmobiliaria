from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    rut = models.CharField(unique=True, max_length=9, validators=[RegexValidator(r'^\d{7,8}[\dK]$')])
    address = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=12)
    user_type = models.ForeignKey(UserType,  on_delete=models.SET_NULL, null=True, blank=True)

    def is_landlord(self):
        return self.user_type and self.user_type.name == 'Arrendador'

    def is_tenant(self):
        return self.user_type and self.user_type.name == 'Arrendatario'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    groups = models.ManyToManyField(
        Group,
        related_name='%(app_label)s_%(class)s_related',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='%(app_label)s_%(class)s_related',
        blank=True,
    )


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Comuna(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='comunas', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    ]

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    total_area = models.PositiveIntegerField(blank=False)
    built_area = models.PositiveIntegerField(blank=False)
    parking = models.PositiveSmallIntegerField(default=0)
    rooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    address = models.CharField(max_length=100, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=False, null=False)
    commune = models.ForeignKey(Comuna, on_delete=models.CASCADE, blank=False, null=False)
    prop_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='departamento')
    price = models.PositiveIntegerField(blank=False)
    owner = models.ForeignKey(User, related_name='owned_properties', on_delete=models.SET_NULL, blank=True, null=True)
    renter = models.ForeignKey(User, related_name='rented_properties', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.URLField(max_length=100,blank=True)
    def __str__(self):
        return f'{self.name} ({self.prop_type}) - Dueño: {self.owner.username if self.owner else "None"}'
