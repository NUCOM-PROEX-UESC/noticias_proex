from django.db import migrations

def add_status_choices(apps, schema_editor):
    News = apps.get_model('news', 'News')
    News.objects.bulk_create([
        News(status='pending', titulo='Exemplo Pending', subtitulo='Pending', lead='Pending', corpo='Pending', criador_id=1),
        News(status='approved', titulo='Exemplo Approved', subtitulo='Approved', lead='Approved', corpo='Approved', criador_id=1),
        News(status='rejected', titulo='Exemplo Rejected', subtitulo='Rejected', lead='Rejected', corpo='Rejected', criador_id=1),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_status_choices),
    ]
