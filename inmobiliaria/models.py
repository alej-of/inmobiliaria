from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator

class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BaseUser(AbstractUser):
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

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    ]

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    total_area = models.PositiveIntegerField(blank=False)
    built_area = models.PositiveIntegerField(blank=False)
    parking = models.PositiveSmallIntegerField(default=0)
    rooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    address = models.CharField(max_length=100, blank=False)
    region = models.CharField(max_length=50, blank=False)
    commune = models.CharField(max_length=20, blank=False)
    
    prop_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='departamento')
    price = models.PositiveIntegerField(blank=False)
    owner = models.ForeignKey(BaseUser, related_name='owned_properties', on_delete=models.SET_NULL, blank=True, null=True)
    renter = models.ForeignKey(BaseUser, related_name='rented_properties', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.prop_type}) - Owner: {self.owner.username if self.owner else "None"}'
