from django.contrib import admin
from django.contrib.auth import get_user_model

# User = get_user_model()
# admin.site.unregister(User)
#
#
# @admin.register(User)
# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'username', 'email', 'first_name',
#                     'last_name', 'is_active', 'is_staff', )
#     search_fields = ('email', 'first_name', 'last_name', 'username',)
#     list_filter = ('is_active', 'is_staff',)
#     empty_value_display = '-not filled-'
#     list_display_links = ('pk', 'username',)
#     date_hierarchy = 'last_login'
#
#     fieldsets = (
#         (None, {
#             'fields': ('first_name', 'last_name', 'username', 'email', 'password', )
#         }),
#         ('Advanced options', {
#             'classes': ('collapse',),
#             'fields': ('date_joined', 'last_login',
#                        'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )
