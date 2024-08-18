from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Property
from .forms import SignUpForm

# Create your views here.
def index(request):
    context = {
    }
    return render(request,'index.html',context)

@login_required
def profile(request):
    context = {
    }
    return render(request,'profile.html',context)

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
    if request.method == 'POST':
        user = request.user
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password:
            if current_password:
                if user.check_password(current_password):
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Tus datos han sido actualizados y la contraseña cambiada correctamente.')
                    else:
                        messages.error(request, 'Las nuevas contraseñas no coinciden.')
                else:
                    messages.error(request, 'La contraseña actual es incorrecta.')
            else:
                messages.error(request, 'Debes proporcionar tu contraseña actual para cambiar la contraseña nueva.')

        user.save()
        messages.success(request, 'Tus datos han sido actualizados correctamente.')
        return redirect('index')

    return render(request, 'index.html')

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
