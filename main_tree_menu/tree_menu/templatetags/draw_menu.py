from django import template
from django.db.models.query import QuerySet
from django.utils.safestring import SafeString
from tree_menu.models import Item

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context: dict, menu: SafeString) -> dict:
    selected_item_slug = context['request'].GET.get(menu, None)

    items = Item.objects.filter(
        menu__title=menu).select_related('menu', 'parent')
    items_values = items.values()

    primary_items = list(items_values.filter(parent=None))

    result_dict = {'items': primary_items, 'menu': menu}

    if selected_item_slug:
        try:
            selected_item = items.get(slug=selected_item_slug)
            selected_item_id_list = get_selected_item_id_list(selected_item)

            for item in primary_items:
                if item['id'] in selected_item_id_list:
                    item['child_items'] = get_child_items(
                        items_values, item['id'], selected_item_id_list)

        except Item.DoesNotExist:
            result_dict['items'] = primary_items
            result_dict['error'] = f"Item with slug '{selected_item_slug}' does not exist."

    return result_dict


def get_child_items(items_values: QuerySet, current_item_id: int, selected_item_id_list: list) -> list:
    item_list = list(items_values.filter(parent_id=current_item_id))

    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_items(
                items_values, item['id'], selected_item_id_list)

    return item_list


def get_selected_item_id_list(selected_item: Item) -> list:
    selected_item_id_list = []

    while selected_item:
        selected_item_id_list.append(selected_item.id)
        selected_item = selected_item.parent

    return selected_item_id_list
