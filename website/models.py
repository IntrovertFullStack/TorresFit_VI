from django.db import models
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserChangeForm



class Datos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='datos')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# Define the Producto model
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    en_oferta = models.BooleanField(default=False)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nombre
     
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

# Rename Categoria to CarritoItem
class CarritoItem(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    sesion_id = models.CharField(max_length=200, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
    def subtotal(self):
        # Use the sale price if available, otherwise use the regular price
        precio = self.producto.precio_oferta if self.producto.precio_oferta else self.producto.precio
        return precio * self.cantidad

# Register models with the admin site
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'usuario', 'sesion_id', 'fecha_creacion']
    list_filter = ['fecha_creacion',]
    search_fields = ['producto__nombre', 'usuario__username']

try:
    admin.site.register(Producto)
    admin.site.register(CarritoItem, CarritoItemAdmin)
except AlreadyRegistered:
    pass

# Assuming Datos is defined elsewhere
class AdminPerfilUsuario(admin.ModelAdmin):
    model = Datos
    list_display = ['usuario', 'nombre', 'apellido']
    
admin.site.register(Datos, AdminPerfilUsuario)

class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')

    def __str__(self):
        return f'{self.usuario.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ordenes')
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    sesion_id = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    metodo_pago = models.CharField(max_length=20, choices=[('nequi', 'Nequi'), ('bancolombia', 'Bancolombia')])
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.IntegerField(default=1)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def subtotal(self):
        return self.precio * self.cantidad