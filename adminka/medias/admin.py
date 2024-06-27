from django.contrib import admin
from .models import User, QuranVerseModel


class UserAdmin(admin.ModelAdmin):
    actions_on_top = False
    list_display = ('full_name', 'username', 'telegram_id')
    ordering = ('full_name',)


class QuranVerseAdmin(admin.ModelAdmin):
    actions_on_top = False
    list_display = ('sura_number', 'sura_name', 'total_verses', )
    ordering = ('sura_number',)


admin.site.register(User, UserAdmin)
admin.site.register(QuranVerseModel, QuranVerseAdmin)
