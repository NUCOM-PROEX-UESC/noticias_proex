# Generated by Django 5.0.6 on 2024-05-25 04:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_newsimage_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='corpo',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
