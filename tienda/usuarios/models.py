from django.db import models


class MensajeContacto(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    email = models.EmailField('Correo electrónico')
    asunto = models.CharField('Asunto', max_length=150)
    mensaje = models.TextField('Mensaje', max_length=2000)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f'{self.asunto} ({self.email})'