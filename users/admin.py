from django.contrib import admin
from .models import Users
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth import admin as auth_admin

@admin.register(Users)
class UsersAdmin(auth_admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Users
    list_display = ['first_name', 'last_name', 'username', 'email', 'perfil', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'perfil']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'perfil')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'email', 'perfil', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)