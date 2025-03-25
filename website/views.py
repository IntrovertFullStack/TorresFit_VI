from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db import transaction, models
from django.conf import settings
from .models import Producto, CarritoItem, Orden, OrdenItem, Datos
from .forms import ProfileUpdateForm, UserForm, CustomUserChangeForm, OrdenForm

import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'website/index.html')

def gallery(request):
    return render(request, 'website/gallery.html')

# def shop(request):
#     productos = Producto.objects.all()
#     return render(request, 'website/shop.html', {'productos': productos})

def producto(request):
    productos = Producto.objects.all()
    return render(request, 'website/product.html', {'productos': productos})

def welcome(request):
    return render(request, 'website/welcome.html')

def merge_cart_items(user, session_id):
    carrito_items = CarritoItem.objects.filter(sesion_id=session_id)
    existing_items = {item.producto_id: item for item in CarritoItem.objects.filter(usuario=user)}

    with transaction.atomic():
        for item in carrito_items:
            if item.producto_id in existing_items:
                existing_item = existing_items[item.producto_id]
                existing_item.cantidad += item.cantidad
                existing_item.save()
                item.delete()
            else:
                item.usuario = user
                item.sesion_id = None
                item.save()

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            session_id = request.session.session_key
            if session_id:
                merge_cart_items(user, session_id)
            return redirect('home')  # Redirigir a la página principal después de iniciar sesión
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    return render(request, 'website/Login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
        }

        if password == confirm_password:
            if len(password) < 8:  # Check the length of the password
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'El nombre de usuario ya existe')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'El correo electrónico ya está registrado')
                else:
                    user = User.objects.create_user(
                        username=username, 
                        password=password, 
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name
                    )
                    messages.success(request, 'Cuenta creada exitosamente')
                    return redirect('login')  # Redirect to login only on successful registration
        else:
            messages.error(request, 'Las contraseñas no coinciden')
        
        # If there are errors, render the registration form again with the context data
        return render(request, 'website/Login.html', context)
    
    # If it's a GET request, just render the registration form
    return render(request, 'website/Login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        print("Form data:", request.POST)  # Debug: Print form data
        print("User form errors:", user_form.errors)  # Debug: Print form errors

        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'website/edit_profile.html', {
        'user_form': user_form,
    })

# def product(request, pk):
#     productos = Producto.objects.get(id=pk)
#     return render(request, 'website/product.html', {'producto': producto})


def restablecer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/contrasena/{uid}/{token}/")
            send_mail(
                "Restablecimiento de Contraseña",
                f"Haz clic en el siguiente enlace para restablecer tu contraseña:\n\n{enlace}",
                "zamasgamer333@gmail.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "Se ha enviado un enlace a tu correo para restablecer tu contraseña.")
            return redirect("login")
        else:
            messages.error(request, "No se encontro un usuario con ese correo electronico.")
            return redirect("restablecer")
        
    return render(request, "website/restablecer.html")


def contrasena(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contrasena = request.POST["password"]
            user.set_password(nueva_contrasena)
            user.save()
            return redirect("password_changed")
        return render(request, "website/contrasena.html")
    return redirect("login")


def password_changed(request):
    return render(request, "website/password_changed.html")


def contactenos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        # Send an email (example)
        send_mail(
            f'Mensaje de {nombre}',
            mensaje,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        
        # Optionally, you can add a success message
        messages.success(request, 'Tu mensaje ha sido enviado.')
        return redirect('contactenos')
    
    return render(request, 'website/contactenos.html')

@login_required
def shop_view(request, producto_id=None):
    # Fetch all products for the related items section
    productos = Producto.objects.all()
    
    # Fetch the selected product (if an ID is provided)
    selected_producto = None
    if producto_id:
        selected_producto = get_object_or_404(Producto, id=producto_id)
    
    context = {
        'productos': productos,
        'selected_producto': selected_producto,
    }
    return render(request, 'website/shop.html', context)

@login_required
def ver_carrito(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    for item in carrito_items:
        total += item.subtotal()
        
    return render (request, 'website/nuevocarrito.html', {'carrito_items': carrito_items, 'total': total})

def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
    
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                if cantidad > item.producto.stock:
                    messages.error(request, f"No hay suficiente stock para {item.producto.nombre}. Stock disponible: {item.producto.stock}")
                else:
                    item.cantidad = cantidad
                    item.save()
                    messages.success(request, 'Carrito actualizado')
            else:
                item.delete()
                messages.success(request, 'Item eliminado del carrito')
        else:
            messages.error(request, 'No tienes permiso para modificar este item')
    except CarritoItem.DoesNotExist:
        messages.error(request, 'El item no existe')
        
    return redirect('ver_carrito')

@login_required
def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
    
        if request.user.is_authenticated and item.usuario == request.user or \
        not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            item.delete()
            messages.success(request, 'Item eliminado')
        else:
            messages.error(request, 'No tienes permiso para eliminar este item')
    except CarritoItem.DoesNotExist:
        messages.error(request, 'Item no encontrado')
        
    return redirect('ver_carrito')

@login_required
def productos(request):
    productos = Producto.objects.all()
    
    # Retrieve cart items for the current user or session
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    # Calculate the total cost of the cart items
    for item in carrito_items:
        total += item.subtotal()
    
    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id')
        try:
            producto = Producto.objects.get(id=producto_id)
            
            # Check if the product is in stock
            if producto.stock <= 0:
                messages.error(request, f"{producto.nombre} está agotado.")
                return redirect('productos')
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    sesion_id=sesion_id,
                    usuario=None
                )
                
                if not created:
                    if carrito_item.cantidad + 1 > producto.stock:
                        messages.error(request, f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")
                    else:
                        carrito_item.cantidad += 1
                        carrito_item.save()
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None
                )
                
                if not created:
                    if carrito_item.cantidad + 1 > producto.stock:
                        messages.error(request, f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")
                    else:
                        carrito_item.cantidad += 1
                        carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito" )
        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado')
            
    return render(request, 'website/shop.html', {
        'productos': productos,
        'carrito_items': carrito_items,
        'total': total
    })

def checkout(request):
    return render(request, 'website/checkout.html')

def user_manual(request):
    return render(request, 'website/user_manual.html')

@login_required
def pasarela(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    total = 0

    # Si el carrito está vacío, mostrar advertencia
    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')

    # Calcular el total del pedido
    for item in carrito_items:
        total += item.subtotal()

    if request.method == 'POST':
        form = OrdenForm(request.POST)
        metodo_pago = request.POST.get('metodo_pago')

        if form.is_valid() and metodo_pago:
            # Validate stock before creating the order
            for item in carrito_items:
                producto = item.producto
                if item.cantidad > producto.stock:
                    messages.error(request, f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")
                    return redirect('ver_carrito')

            # If all items have sufficient stock, proceed to create the order
            orden = form.save(commit=False)
            orden.usuario = request.user  # Ensure usuario is set
            orden.total = total
            orden.metodo_pago = metodo_pago
            orden.save()

            # Guardar los productos en la orden y update stock
            for item in carrito_items:
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()

                OrdenItem.objects.create(
                    orden=orden,
                    producto=item.producto,
                    precio=item.producto.precio,
                    cantidad=item.cantidad
                )

            # Vaciar el carrito después del pago
            carrito_items.delete()

            # Enviar el correo de confirmación
            try:
                enviar_correo_confirmacion(orden)
                messages.success(request, "Tu pedido ha sido procesado con éxito. Se ha enviado un correo de confirmación.")
            except Exception as e:
                logger.error(f"Error al enviar el correo de confirmación: {e}")
                messages.error(request, "Hubo un error al enviar el correo de confirmación. Por favor, contacta al soporte.")

            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmar', orden_id=orden.id)
        else:
            if not metodo_pago:
                messages.error(request, "Por favor selecciona un método de pago válido.")
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        # Precargar los datos del usuario en el formulario
        try:
            datos = Datos.objects.get(usuario=request.user)
            initial_data = {
                'nombre': f"{datos.nombre} {datos.apellido}",
                'email': request.user.email
            }
        except Datos.DoesNotExist:
            initial_data = {
                'nombre': request.user.username,
                'email': request.user.email
            }

        form = OrdenForm(initial=initial_data)

    return render(request, 'website/pasarela.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })

@login_required
def confirmacion(request, orden_id):
    try:
        orden = Orden.objects.get(id=orden_id, usuario=request.user)
        items = OrdenItem.objects.filter(orden=orden)

        return render(request, 'website/confirmar.html', {
            'orden': orden,
            'items': items
        })
    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada")
        return redirect('productos')

def enviar_correo_confirmacion(orden):
    """ Envía un correo de confirmación al cliente """
    asunto = f"Confirmación de Pedido #{orden.id}"
    mensaje = f"""
    Hola {orden.nombre},
    Gracias por tu compra. Hemos recibido tu pedido y te hemos enviado un correo electrónico con los detalles de confirmación.
    🌟 **Detalles del Pedido**
    – Número de Pedido: {orden.id}
    – Total: ${orden.total}
    – Método de Pago: {orden.get_metodo_pago_display()}
    – Fecha: {orden.fecha_creacion.strftime("%d/%m/%Y %H:%M")}
    🌟 **Productos Comprados**:
    """
    # Agregar productos al mensaje
    items = OrdenItem.objects.filter(orden=orden)
    for item in items:
        mensaje += f"\n    – {item.cantidad} x {item.producto.nombre} (${item.precio} c/u)"
    mensaje += "\n\nGracias por confiar en nosotros. 😊\n\nSaludos,\nTu tienda online"

    try:
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,  # Use the default email from settings
            [orden.email],  # Use orden.email instead of orden.usuario.email
            fail_silently=False,
        )
        logger.info(f"Correo enviado exitosamente a {orden.email}")
    except Exception as e:
        logger.error(f"Error al enviar el correo de confirmación: {e}")

@login_required
def shopping_history(request):
    # Fetch all orders for the logged-in user
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Prepare the context to pass to the template
    context = {
        'ordenes': ordenes,
    }
    
    return render(request, 'website/historial.html', context)
