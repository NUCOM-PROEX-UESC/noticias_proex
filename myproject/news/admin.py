from django.contrib import admin
from .models import News, NewsImage

class NewsImageInline(admin.TabularInline):
    model = NewsImage

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]

admin.site.register(News, NewsAdmin)
admin.site.register(NewsImage)
