from ninja import Router, Schema
from ninja.security import django_auth
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Producto, Categoria, Marca
from .serializers import ProductoSerializer, CategoriaSerializer, MarcaSerializer
import jwt
from rest_framework.exceptions import AuthenticationFailed

# Crear el router
router = Router()

# Esquemas de salida
class ProductoOut(Schema):
    codigo: str
    nombre: str
    precio: float
    categoria: str
    marca: str

class CategoriaOut(Schema):
    id: int
    nombre: str

class MarcaOut(Schema):
    id: int
    nombre: str

# Obtener listado de categorías
@router.get("/categorias", response=list[CategoriaOut])
def obtener_categorias(request):
    categorias = Categoria.objects.all()
    return categorias

# Obtener listado de marcas
@router.get("/marcas", response=list[MarcaOut])
def obtener_marcas(request):
    marcas = Marca.objects.all()
    return marcas

# Obtener listado de productos
@router.get("/productos", response=list[ProductoOut])
def obtener_productos(request, categoria: int = None, marca: int = None):
    productos = Producto.objects.all()
    if categoria:
        productos = productos.filter(categoria_id=categoria)
    if marca:
        productos = productos.filter(marca_id=marca)
    return productos

# Obtener detalle de un producto
@router.get("/producto/{codigo}", response=ProductoOut)
def obtener_detalle_producto(request, codigo: str):
    producto = get_object_or_404(Producto, codigo=codigo)
    return producto

# Modificar un producto (requiere JWT)
@router.patch("/producto/{codigo}", response=ProductoOut, auth=django_auth)
def modificar_producto(request, codigo: str, producto_data: ProductoOut):
    producto = get_object_or_404(Producto, codigo=codigo)
    for key, value in producto_data.dict().items():
        setattr(producto, key, value)
    producto.save()
    return producto

# Obtener el token JWT
@router.post("/token")
def obtener_token(request, username: str, password: str):
    user = get_object_or_404(User, username=username)
    if not user.check_password(password):
        raise AuthenticationFailed("Credenciales inválidas")
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


