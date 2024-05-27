from django.urls import path
from .views import NewsCreateView, NewsImageCreateView, NewsListView, PendingNewsListView, NewsDetailView, ApprovedNewsListView, ImageUploadView
from .views import NewsPendingListView, NewsDetailView, approve_news, reject_news

urlpatterns = [
    path('pending/', NewsPendingListView.as_view(), name='news-pending'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/approve/', approve_news, name='approve-news'),
    path('<int:pk>/reject/', reject_news, name='reject-news'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:id>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/pending/', PendingNewsListView.as_view(), name='pending-news'),
    path('news/approved/', ApprovedNewsListView.as_view(), name='approved-news'),
    path('image-upload/', ImageUploadView.as_view(), name='image-upload'),
]
