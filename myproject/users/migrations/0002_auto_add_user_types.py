from django.db import migrations

def add_user_types(apps, schema_editor):
    UserType = apps.get_model('users', 'UserType')
    UserType.objects.create(name="Administrador")
    UserType.objects.create(name="Moderador")
    UserType.objects.create(name="Criador de Conteúdo")
    UserType.objects.create(name="Coordenador")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_user_types),
    ]
