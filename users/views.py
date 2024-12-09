from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def register_view(request):
    if request.method == "POST":
        # Obtener datos del formulario
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Validaciones básicas
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register")

        if len(password) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return redirect("register")

        # Crear el usuario
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Hashear la contraseña
        )
        messages.success(
            request, "Usuario registrado exitosamente. ¡Ahora puedes iniciar sesión!"
        )
        return redirect("index")

    return render(request, "users/register.html")


def login_view(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        username = request.POST["username"]
        password = request.POST["password"]

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Iniciar sesión si las credenciales son correctas
            login(request, user)
            return redirect("index")  # Redirigir a la página principal
        else:
            # Mostrar un error si las credenciales no son válidas
            messages.error(request, "Email o contraseña incorrectos.")

    # Mostrar el formulario de inicio de sesión
    return render(request, "users/login.html")


def account_view(request):
    # Mostrar la información del usuario
    
    return render(request, "users/info.html")


@login_required
def logout_view(request):
        logout(request)
        return redirect("login")
