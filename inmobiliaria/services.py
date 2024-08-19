from .models import Property

def create_property(name, description, total_area, built_area, parking, rooms, bathrooms, address, region, commune, prop_type, price, image, owner):
    try:
        property = Property.objects.create(
            name=name,
            description=description,
            total_area=total_area,
            built_area=built_area,
            parking=parking,
            rooms=rooms,
            bathrooms=bathrooms,
            address=address,
            region = region,
            commune=commune,
            prop_type=prop_type,
            price=price,
            image=image,
            owner=owner
        )
        return property
    except Exception as e:
        print(f"Error al crear propiedad: {e}")
        return None

def recall_property(id):
    try:
        return Property.objects.get(id=id)
    except Property.DoesNotExist:
        print(f"No existe la propiedad con ID {id} en la base de datos.")
        return None
    except Exception as e:
        print(f"Error al buscar la propiedad: {e}")
        return None

def update_property(id, name=None, description=None, total_area=None, built_area=None, parking=None, rooms=None, bathrooms=None, address=None, commune=None, prop_type=None, price=None):
    try:
        property = Property.objects.get(id=id)
        if name is not None:
            property.name = name
        if description is not None:
            property.description = description
        if total_area is not None:
            property.total_area = total_area
        if built_area is not None:
            property.built_area = built_area
        if parking is not None:
            property.parking = parking
        if rooms is not None:
            property.rooms = rooms
        if bathrooms is not None:
            property.bathrooms = bathrooms
        if address is not None:
            property.address = address
        if commune is not None:
            property.commune = commune
        if prop_type is not None:
            property.prop_type = prop_type
        if price is not None:
            property.price = price
        property.save()
        return property
    except Property.DoesNotExist:
        print(f"No existe la propiedad con ID {id} en la base de datos.")
        return None
    except Exception as e:
        print(f"Error al actualizar la propiedad: {e}")
        return None

def delete_property(id):
    try:
        property = Property.objects.get(id=id)
        property.delete()
        return True
    except Property.DoesNotExist:
        print(f"No existe la propiedad con ID {id} en la base de datos.")
        return False
    except Exception as e:
        print(f"Error al eliminar la propiedad: {e}")
        return False
