from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             verbose_name='Заголовок меню')
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255)
    menu = models.ForeignKey(Menu, blank=True, related_name='items',
                             on_delete=models.CASCADE, verbose_name='Основное меню')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childrens',
                               on_delete=models.CASCADE, verbose_name='Подменю')

    class Meta:
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'

    def __str__(self):
        return self.title
