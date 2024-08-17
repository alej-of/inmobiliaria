import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto.settings')
django.setup()

from inmobiliaria.models import Property, Region, Comuna

def list_communes_with_properties_without_renter():
    communes_by_region = {}
    regions = Region.objects.all()

    for region in regions:
        communes = Comuna.objects.filter(region=region)
        communes_with_properties = {}

        for commune in communes:
            properties = Property.objects.filter(commune=commune, renter__isnull=True)

            if properties.exists():
                communes_with_properties[commune.name] = list(properties.values('name', 'address', 'price', 'prop_type'))

        if communes_with_properties:
            communes_by_region[region.name] = communes_with_properties

    return communes_by_region

def save_results_to_file(results, filename):
    with open(filename, 'w',encoding='utf-8') as file:
        for region, communes in results.items():
            file.write(f"Región: {region}\n")
            for commune, properties in communes.items():
                file.write(f"  Comuna: {commune}\n")
                for prop in properties:
                    file.write(f"    Propiedad: {prop['name']}, Tipo: {prop['prop_type']}, Dirección: {prop['address']}, Precio: ${prop['price']}\n")
                file.write("\n")
            file.write("\n")

if __name__ == "__main__":
    communes_by_region = list_communes_with_properties_without_renter()
    save_results_to_file(communes_by_region, 'vacant_properties_by_commune.txt')
    print("Results have been saved to 'vacant_properties_by_commune.txt'.")
