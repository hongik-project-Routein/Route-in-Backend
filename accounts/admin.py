from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class CustomUserAdmin(UserAdmin):
    # 폼 설정
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('id', 'uname', 'email', 'name', 'age', 'gender', 'joined_at',)
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('uname', 'name', 'age', 'gender', 'image')}),
        ('Relationships', {'fields': ('sim_users',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('id',)
    filter_horizontal = ()



admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)