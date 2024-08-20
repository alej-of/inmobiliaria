# Generated by Django 5.0.7 on 2024-08-20 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmobiliaria', '0004_property_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tipoinmueble',
        ),
        migrations.AddField(
            model_name='property',
            name='lease_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='lease_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
