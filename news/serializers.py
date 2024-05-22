from rest_framework import serializers
from .models import News, Image

from rest_framework import serializers
from .models import News, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        news = News.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(news=news, **image_data)
        return news

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)

        for image_data in images_data:
            image = Image.objects.create(news=instance, **image_data)
            image.save()

        return instance