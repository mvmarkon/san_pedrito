from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioModelTests(TestCase):
    """Pruebas para el modelo Usuario"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='test@example.com',
            password='testpassword',
            nombre='Test',
            apellido='User',
            rol='VENDEDOR'
        )
        
        self.admin = Usuario.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            nombre='Admin',
            apellido='User'
        )
    
    def test_create_user(self):
        """Prueba la creación de un usuario normal"""
        self.assertEqual(self.usuario.email, 'test@example.com')
        self.assertEqual(self.usuario.nombre, 'Test')
        self.assertEqual(self.usuario.apellido, 'User')
        self.assertEqual(self.usuario.rol, 'VENDEDOR')
        self.assertTrue(self.usuario.is_active)
        self.assertFalse(self.usuario.is_staff)
        self.assertFalse(self.usuario.is_superuser)
        self.assertTrue(self.usuario.is_vendedor)
        self.assertFalse(self.usuario.is_admin)
        self.assertFalse(self.usuario.is_inventario)
    
    def test_create_superuser(self):
        """Prueba la creación de un superusuario"""
        self.assertEqual(self.admin.email, 'admin@example.com')
        self.assertEqual(self.admin.rol, 'ADMIN')
        self.assertTrue(self.admin.is_active)
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.admin.is_admin)
        self.assertFalse(self.admin.is_vendedor)
        self.assertFalse(self.admin.is_inventario)
    
    def test_get_full_name(self):
        """Prueba el método get_full_name"""
        self.assertEqual(self.usuario.get_full_name(), 'Test User')
    
    def test_get_short_name(self):
        """Prueba el método get_short_name"""
        self.assertEqual(self.usuario.get_short_name(), 'Test')
    
    def test_str_representation(self):
        """Prueba la representación en cadena del usuario"""
        self.assertEqual(str(self.usuario), 'Test User')

class UsuarioAPITests(APITestCase):
    """Pruebas para la API de Usuario"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email='test@example.com',
            password='testpassword',
            nombre='Test',
            apellido='User',
            rol='VENDEDOR'
        )
        
        self.admin = Usuario.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            nombre='Admin',
            apellido='User'
        )
        
        self.client.credentials()
    
    def test_login(self):
        """Prueba el inicio de sesión y la obtención de tokens"""
        url = reverse('token_obtain_pair')
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_get_user_list_unauthenticated(self):
        """Prueba que un usuario no autenticado no puede ver la lista de usuarios"""
        url = reverse('usuario-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_list_authenticated(self):
        """Prueba que un usuario autenticado puede ver la lista de usuarios"""
        self.client.force_authenticate(user=self.usuario)
        url = reverse('usuario-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Hay 2 usuarios en la base de datos
    
    def test_create_user_as_admin(self):
        """Prueba que un administrador puede crear usuarios"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('usuario-list')
        data = {
            'email': 'new@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword',
            'nombre': 'New',
            'apellido': 'User',
            'rol': 'INVENTARIO',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 3)
    
    def test_create_user_as_non_admin(self):
        """Prueba que un usuario no administrador no puede crear usuarios"""
        self.client.force_authenticate(user=self.usuario)
        url = reverse('usuario-list')
        data = {
            'email': 'new@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword',
            'nombre': 'New',
            'apellido': 'User',
            'rol': 'INVENTARIO',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Usuario.objects.count(), 2)
    
    def test_update_own_profile(self):
        """Prueba que un usuario puede actualizar su propio perfil"""
        self.client.force_authenticate(user=self.usuario)
        url = reverse('usuario-perfil')
        data = {
            'nombre': 'Updated',
            'apellido': 'Name',
            'telefono': '+1234567890'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nombre, 'Updated')
        self.assertEqual(self.usuario.apellido, 'Name')
        self.assertEqual(self.usuario.telefono, '+1234567890')
    
    def test_change_password(self):
        """Prueba el cambio de contraseña"""
        self.client.force_authenticate(user=self.usuario)
        url = reverse('usuario-cambiar-password', args=[self.usuario.id])
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword123',
            'new_password_confirm': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la contraseña ha cambiado intentando iniciar sesión
        self.client.credentials()
        url = reverse('token_obtain_pair')
        data = {'email': 'test@example.com', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)