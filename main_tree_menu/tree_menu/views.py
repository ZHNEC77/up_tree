from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import Item


class IndexPageView(TemplateView):
    template_name = 'tree_menu/index.html'


def redirect_view(request: HttpRequest, slug) -> HttpResponse:
    item = Item.objects.get(slug=slug)
    return render(request, 'tree_menu/detail_menu.html', context={'item': item})
