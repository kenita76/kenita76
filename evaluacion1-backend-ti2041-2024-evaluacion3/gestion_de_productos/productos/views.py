from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def index(request):
    productos = Producto.objects.all()
    return render(request, 'templates/index.html', {'productos': productos})

@staff_member_required
def registro(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resultado')
    else:
        form = ProductoForm()
    return render(request, 'templates/registro.html', {'form': form})

@login_required
def resultado(request):
    producto = None
    error = None
    if request.method == 'POST':
        producto_id = request.POST.get('id')
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            error = "Producto no encontrado"
    return render(request, 'templates/resultado.html', {'producto': producto, 'error': error})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'templates/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')