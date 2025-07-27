from django import template
from django.utils.safestring import SafeString
from tree_menu.models import Item

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context: dict, menu: SafeString) -> dict:
    selected_item_slug = context['request'].GET.get(menu, None)

    # Один запрос к БД для всех элементов меню
    items = Item.objects.filter(
        menu__title=menu).select_related('parent', 'menu')
    items_list = list(items)

    # Создаем словарь для быстрого доступа и собираем дерево
    items_dict = {}
    root_items = []

    for item in items_list:
        items_dict[item.id] = item
        if not hasattr(item, 'child_items'):
            item.child_items = []

        if item.parent_id:
            if item.parent_id in items_dict:
                parent = items_dict[item.parent_id]
                if not hasattr(parent, 'child_items'):
                    parent.child_items = []
                parent.child_items.append(item)
        else:
            root_items.append(item)

    # Помечаем путь к выбранному элементу
    if selected_item_slug:
        selected_item = next(
            (item for item in items_list if item.slug == selected_item_slug), None)
        if selected_item:
            # Поднимаемся вверх по родителям, помечая их
            current = selected_item
            while current:
                current.is_open = True
                current = items_dict.get(
                    current.parent_id) if current.parent_id else None

    return {'items': root_items, 'menu': menu}
