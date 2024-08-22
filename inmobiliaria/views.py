from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate,logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from .models import User, Property, Comuna, Region
from .forms import SignUpForm, PropertyForm, UserChangeForm
import inmobiliaria.services as s

# Create your views here.

def index(request):
    properties = Property.objects.filter(renter__isnull=True)
    prop_type = request.GET.get('prop_type')
    region_id = request.GET.get('region')
    commune_id = request.GET.get('commune')

    if prop_type:
        properties = properties.filter(prop_type=prop_type)
    if region_id:
        properties = properties.filter(region_id=region_id)
    if commune_id:
        properties = properties.filter(commune_id=commune_id)

    regions = Region.objects.all()
    comunas = Comuna.objects.filter(region_id=region_id) if region_id else Comuna.objects.none()

    context = {
        'properties': properties,
        'regions': regions,
        'comunas': comunas,
        'selected_type': prop_type,
        'selected_region': region_id,
        'selected_commune': commune_id,
    }

    return render(request, 'index.html', context)

@login_required
def profile(request):
    user = request.user
    prop = Property.objects.none()
    if user.is_landlord:
        prop = prop | Property.objects.filter(owner=user.id)
    if user.is_tenant:
        prop = prop | Property.objects.filter(renter=user.id)

    context = {
        'properties': prop.distinct()
    }
    return render(request, 'profile.html', context)

def add_property(request):
    regions = Region.objects.all()
    region_id = request.GET.get('region')
    comunas = Comuna.objects.filter(region_id=region_id) if region_id else Comuna.objects.none()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            total_area = form.cleaned_data.get('total_area')
            built_area = form.cleaned_data.get('built_area')
            parking = form.cleaned_data.get('parking')
            rooms = form.cleaned_data.get('rooms')
            bathrooms = form.cleaned_data.get('bathrooms')
            address = form.cleaned_data.get('address')
            region = form.cleaned_data.get('region')
            commune = form.cleaned_data.get('commune')
            prop_type = form.cleaned_data.get('prop_type')
            price = form.cleaned_data.get('price')
            image = form.cleaned_data.get('image')

            property = s.create_property(name, description, total_area, built_area, parking, rooms, bathrooms, address, region, commune, prop_type, price, image, request.user)
            if property:
                messages.success(request, 'Propiedad creada con éxito.')
                return redirect('perfil')
            else:
                messages.error(request, 'Hubo un error al crear la propiedad.')
    else:
        form = PropertyForm()
    context = {
        'form': form,
        'regions': regions,
        'comunas' : comunas,
    }

    return render(request, 'add_property.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciado sesión correctamente.')
                return redirect('index')
        else:
            
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                messages.error(request, 'Usuario no encontrado. Asegúrate de que esté correcto.')
            else:
                messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')
                
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('index')

@login_required
def update_account(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()

            if request.POST.get('new_password1'):
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Tus datos han sido actualizados y la contraseña cambiada correctamente.')
            else:
                messages.success(request, 'Tus datos han sido actualizados correctamente.')

            return redirect('perfil')


        else:
            user_form_errors = "".join([f"<li>{field.label}: {error}</li>" for field in user_form for error in field.errors])
            password_form_errors = "".join([f"<li>{field.label}: {error}</li>" for field in password_form for error in field.errors])
            error_message = "<p>Por favor, corrige los errores en el formulario:</p><ul>"
            if user_form_errors:
                error_message += user_form_errors
            if password_form_errors:
                error_message += password_form_errors
            error_message += "</ul>"

            messages.error(request, error_message)

    else:
        user_form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)

    context = {
        'user_form': user_form,
        'password_form': password_form
    }

    return render(request, 'profile.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    context = {
        'form' : form,
    }

    return render(request, 'signup.html', context)

def get_comunas(request, region_id):
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(comunas), safe=False)

def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'edit_property.html', {'form': form})


def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, owner=request.user)
    if request.method == 'POST':
        deleted = s.delete_property(property_id)
        if deleted:
            messages.success(request, f'Propiedad "{property.name}" eliminada correctamente.')
        return JsonResponse({'success': True})
    messages.error(request, 'Error al eliminar propiedad')
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def start_lease(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.user.is_authenticated and request.user.is_tenant:
        if property.renter is None:
            property.renter = request.user
            property.lease_start_date = date.today()
            property.save()
            messages.success(request, f'Has arrendado la propiedad "{property.name}".')
        else:
            messages.error(request, f'La propiedad "{property.name}" no está disponible.')
    else:
        messages.error(request, f'No tienes autorización para rentar la propiedad "{property.name}".')

    return redirect('perfil')

def end_lease(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.user.is_authenticated:
        if property.renter == request.user or property.owner==request.user:
            property.renter = None
            property.lease_end_date = date.today()
            property.save()
            messages.success(request, f'Finalizaste el arriendo de la propiedad "{property.name}"')
        else:
            messages.error(request, 'No tienes autorización para finalizar el arriendo de esta propiedad.')

    return redirect('perfil')