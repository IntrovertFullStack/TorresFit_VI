from django.contrib import admin
from django.urls import path
from website import views
from website.views import shop_view
from website.views import edit_profile  # Import the edit_profile view



urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home', views.home, name='home'),
    # path('newhome/', views.newhome, name='newhome'),
    path('gallery/', views.gallery, name='gallery'),
    # path('shop/', views.shop, name='shop'),
    path('shop/<int:producto_id>/', shop_view, name='shop_view'),
    path('producto/<int:pk>', views.producto, name='producto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('restablecer/', views.restablecer, name='restablecer'),
    path('contrasena/<uidb64>/<token>/', views.contrasena, name='contrasena'),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('contactenos/', views.contactenos, name='contactenos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('productos/', views.productos, name='productos'),
    path('checkout/', views.checkout, name='checkout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_manual/', views.user_manual, name='user_manual'),
    path("pasarela/", views.pasarela, name='pasarela'),
    path('confirmacion/<int:orden_id>/', views.confirmacion, name='confirmar'),
    path('shopping_history/', views.shopping_history, name='shopping_history'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/add-user/', views.add_user, name='add_user'),
    path('quick_edit_user/<int:pk>/', views.quick_edit_user, name='quick_edit_user'),
    path('admin-panel/delete-user/<int:pk>/', views.delete_user, name='delete_user'),



]
# Asegúrate de tener una vista para la página principal
