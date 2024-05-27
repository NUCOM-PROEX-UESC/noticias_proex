from rest_framework import generics, permissions, serializers
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import News, NewsImage
from .serializers import NewsSerializer, NewsImageSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import NewsImage
from .serializers import NewsImageSerializer
import logging
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        news = serializer.save(criador=self.request.user)
        card_image = self.request.FILES.get('cardImage')
        if card_image:
            NewsImage.objects.create(news=news, image=card_image, image_type='card')

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class PendingNewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return News.objects.filter(status='pending')

class NewsDetailView(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'status' in data and data['status'] == 'rejected':
            instance.motivo_rejeicao = data.get('motivo_rejeicao', '')
        if 'status' in data and data['status'] == 'approved':
            instance.supervisor = request.user
        instance.status = data.get('status', instance.status)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ApprovedNewsListView(generics.ListAPIView):
    queryset = News.objects.filter(status='approved')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class NewsImageCreateView(generics.CreateAPIView):
    queryset = NewsImage.objects.all()
    serializer_class = NewsImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        logger.debug("Recebendo dados para upload de imagem: %s", request.data)
        news_id = request.data.get('news_id')
        if 'file' in request.data:
            file_data = request.data['file']
            logger.debug("Arquivo recebido: %s", file_data)
        else:
            logger.error("Nenhum arquivo recebido.")
            return Response({"detail": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'image': file_data,
            'image_type': 'default',
            'news': news_id
        }

        file_serializer = NewsImageSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save()
            image_url = request.build_absolute_uri(file_serializer.instance.image.url)
            logger.debug("Upload de imagem bem-sucedido: %s", image_url)
            return Response({'link': image_url}, status=status.HTTP_201_CREATED)
        else:
            logger.error("Erro ao validar dados do upload de imagem: %s", file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class NewsPendingListView(generics.ListAPIView):
    queryset = News.objects.filter(status='pendente')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def approve_news(request, pk):
    try:
        news = News.objects.get(pk=pk)
        news.status = 'aprovada'
        news.save()
        return Response(status=status.HTTP_200_OK)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reject_news(request, pk):
    try:
        news = News.objects.get(pk=pk)
        news.status = 'rejeitada'
        news.motivo_rejeicao = request.data.get('motivo_rejeicao')
        news.save()
        return Response(status=status.HTTP_200_OK)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)