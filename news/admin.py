from django.contrib import admin
from django import forms
from .models import News, Image
from ckeditor.widgets import CKEditorWidget

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class NewsAdminForm(forms.ModelForm):
    lead = forms.CharField(widget=CKEditorWidget())
    corpo = forms.CharField(widget=CKEditorWidget())
    fechamento = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    inlines = [ImageInline]

admin.site.register(News, NewsAdmin)
admin.site.register(Image)
