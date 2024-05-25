from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings

class News(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    lead = models.CharField(max_length=255)
    corpo = RichTextField()
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_created')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_supervised')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    motivo_rejeicao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class NewsImage(models.Model):
    IMAGE_TYPE_CHOICES = (
        ('card', 'Card'),
        ('default', 'Default'),
    )

    image = models.ImageField(upload_to='news_images/')
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.news.titulo if self.news else 'No News'} - {self.image_type}"
