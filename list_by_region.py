import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto.settings')

django.setup()

from inmobiliaria.models import Property, Region

def list_properties_without_renter():
    regions = Region.objects.all()
    properties_by_region = {}
    for region in regions:
        properties = Property.objects.filter(region=region, renter__isnull=True)
        if properties.exists():
            properties_by_region[region.name] = list(properties.values('name', 'address', 'price'))
    return properties_by_region

def save_results_to_file(results, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for region, properties in results.items():
            file.write(f"Región: {region}\n")
            for prop in properties:
                file.write(f"  Propiedad: {prop['name']}, Dirección: {prop['address']}, Precio: ${prop['price']}\n")
            file.write("\n")

if __name__ == "__main__":
    
    properties_by_region = list_properties_without_renter()
    save_results_to_file(properties_by_region, 'vacant_properties_by_region.txt')
    print("Results have been saved to 'vacant_properties_by_region.txt'.")
