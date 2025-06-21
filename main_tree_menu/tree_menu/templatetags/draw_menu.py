from django import template
from django.db.models.query import QuerySet
from django.template.context import RequestContext
from django.utils.safestring import SafeString

from tree_menu.models import Item


register = template.Library()
primary_item = None
selected_item = None


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu: SafeString) -> dict:
    global primary_item, selected_item
    selected_item_slug = None

    items = Item.objects.filter(
        menu__title=menu).select_related('menu', 'parent')
    items_values = items.values()

    try:
        selected_item_slug = context['request'].GET[menu]
        primary_item = [item for item in items_values.filter(parent=None)]
        selected_item = items.get(slug=selected_item_slug)
        selected_item_id_list = get_selected_item_id_list(parent=selected_item,
                                                          primary_item_list=primary_item,
                                                          selected_item_slug=selected_item_slug)

        for item in primary_item:
            if item['id'] in selected_item_id_list:
                item['child_items'] = get_child_items(items_values=items_values,
                                                      current_item_id=item['id'],
                                                      selected_item_id_list=selected_item_id_list)
        result_dict = {'items': primary_item}

    except Exception:
        result_dict = {
            'items': [
                item for item in Item.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    result_dict['menu'] = menu

    if selected_item_slug is not None and len(selected_item_slug) > 0 and selected_item.childrens.count() == 0:
        result = {'slug': selected_item_slug, 'title': items.filter(
            slug=selected_item_slug).get().title}
        return result
    else:
        return result_dict


def get_child_items(items_values: QuerySet, current_item_id: int, selected_item_id_list: list) -> list:
    item_list = [item for item in items_values.filter(
        parent_id=current_item_id)]

    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_items(
                items_values, item['id'], selected_item_id_list)
    if len(item_list) > 0:
        return item_list


def get_selected_item_id_list(parent: Item, primary_item_list: list, selected_item_slug: str) -> list:
    selected_item_slug_list = []

    while parent:
        selected_item_slug_list.append(parent.id)
        parent = parent.parent
    if not selected_item_slug_list:
        for item in primary_item_list:
            if item['slug'] == selected_item_slug:
                selected_item_slug_list.append(selected_item_slug)
    return selected_item_slug_list
