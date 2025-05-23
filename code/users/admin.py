from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from .models import User
from .utils import fetch_users
from django.shortcuts import redirect
from django.utils.html import format_html

# @admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'customer')
    list_filter = ('is_active', 'is_staff', 'customer')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Customer', {'fields': ('customer',)}),
        ('Freshdesk info', {'fields': ('freshdesk_id',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('fetch-create-users/', self.admin_site.admin_view(self.fetch_and_create_users_action), name='fetch-create-users'),
        ]
        return custom_urls + urls

    def fetch_and_create_users_action(self, request):
        message = fetch_users()
        self.message_user(request, message)
        return redirect('..')

    def fetch_and_create_users_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Fetch and Create Users</a>',
            '/admin/users/fetch-create-users/'
        )
    fetch_and_create_users_button.short_description = 'Fetch and Create Users'
    fetch_and_create_users_button.allow_tags = True

    change_list_template = 'users/change_list_with_button.html'

admin.site.register(User, CustomUserAdmin)
