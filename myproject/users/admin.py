from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserType

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'matricula', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('User Types', {'fields': ('user_types',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'matricula', 'password1', 'password2', 'user_types')}
        ),
    )
    list_display = ('username', 'full_name', 'matricula', 'is_staff')
    search_fields = ('username', 'full_name', 'matricula')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Atualizar campos is_staff e is_superuser conforme os tipos de usuário
        if UserType.objects.filter(name='Administrador').exists():
            admin_type = UserType.objects.get(name='Administrador')
            if admin_type in obj.user_types.all():
                obj.is_staff = True
                obj.is_superuser = True
            else:
                obj.is_staff = False
                obj.is_superuser = False
        obj.save()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserType)
