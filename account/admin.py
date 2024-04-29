from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'created_date')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'passwoord')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'modified_date', 'created_date')}),
        ('Personal Datas', {'fields': ('first_name', 'last_name', 'avatar')})
    )
    date_hierarchy = 'created_date'
    readonly_fields = ('last_login', 'modified_date', 'created_date')
    filter_horizontal = ('groups', 'user_permissions')
    list_editable = ('is_active', 'is_staff', 'is_superuser')