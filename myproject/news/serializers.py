from rest_framework import serializers
from .models import News, NewsImage

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'image_type', 'news']

class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'titulo', 'subtitulo', 'lead', 'corpo', 'criador', 'supervisor', 'status', 'motivo_rejeicao', 'images']
        read_only_fields = ['criador', 'supervisor', 'status', 'motivo_rejeicao']
