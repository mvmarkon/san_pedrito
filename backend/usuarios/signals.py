from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    """Actualiza el campo ultimo_acceso cuando un usuario inicia sesión."""
    user.ultimo_acceso = timezone.now()
    user.save(update_fields=['ultimo_acceso'])