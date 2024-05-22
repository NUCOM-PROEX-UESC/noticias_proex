from django.db import models
from ckeditor.fields import RichTextField

class News(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, blank=True, null=True)
    lead = RichTextField()
    corpo = RichTextField()
    fechamento = RichTextField(blank=True, null=True)
    autor = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100, blank=True, null=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_ultima_alteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Image(models.Model):
    MINIATURA = 'miniatura'
    POST = 'post'
    BANNER = 'banner'
    DEFAULT = 'default'
    
    IMAGE_CHOICES = [
        (MINIATURA, 'Miniatura'),
        (POST, 'Post'),
        (BANNER, 'Banner'),
        (DEFAULT, 'Default'),
    ]

    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image_type = models.CharField(max_length=20, choices=IMAGE_CHOICES)
    image = models.ImageField(upload_to='news_images/')

    def __str__(self):
        return f"{self.image_type} for {self.news.titulo}"
