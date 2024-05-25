from django.urls import path
from .views import NewsCreateView, NewsImageCreateView, NewsListView, PendingNewsListView, NewsDetailView, ApprovedNewsListView, ImageUploadView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:id>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/pending/', PendingNewsListView.as_view(), name='pending-news'),
    path('news/approved/', ApprovedNewsListView.as_view(), name='approved-news'),
    path('image-upload/', ImageUploadView.as_view(), name='image-upload'),
]
