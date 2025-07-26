from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import Item, Menu  # Assuming Menu is the model for menus


class IndexPageView(TemplateView):
    template_name = 'tree_menu/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menus = Menu.objects.all()
        context['menus'] = menus
        context['all_items'] = list(
            Item.objects.select_related('parent', 'menu').all())
        return context


def redirect_view(request: HttpRequest, slug) -> HttpResponse:
    item = Item.objects.get(slug=slug)
    return render(request, 'tree_menu/detail_menu.html', context={'item': item})
