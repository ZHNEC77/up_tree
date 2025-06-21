from django.contrib import admin

from .models import Menu, Item


@admin.register(Item)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_id', 'parent')
    list_filter = ('menu',)
    fieldsets = (
        ('Добавление нового элемента меню', {
            'description': "Родителем должно быть основное меню или основное меню и подменю",
            'fields': (('menu', 'parent'), 'title', 'slug')
        }),
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
