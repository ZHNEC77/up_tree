from django import template
from tree_menu.models import Item

register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu):
    # Загружаем все элементы меню одним запросом
    items = list(Item.objects.filter(menu__title=menu))

    items_by_id = {item.id: item for item in items}

    # Инициализируем список детей
    for item in items:
        item.child_items = []

    # Строим дерево
    root_items = []
    for item in items:
        if item.parent_id:
            parent = items_by_id.get(item.parent_id)
            if parent:
                parent.child_items.append(item)
        else:
            root_items.append(item)

    # Определяем выбранный элемент и путь к нему
    selected_slug = context['request'].GET.get(menu)
    selected_item = None
    selected_path_ids = set()

    if selected_slug:
        selected_item = next(
            (item for item in items if item.slug == selected_slug), None)
        current = selected_item
        while current:
            selected_path_ids.add(current.id)
            current = items_by_id.get(current.parent_id)

    # Отмечаем выбранные элементы
    def mark_selected(items):
        for item in items:
            item.is_selected = item.id in selected_path_ids
            mark_selected(item.child_items)

    mark_selected(root_items)

    return {
        'items': root_items,
        'menu': menu,
        'selected_item': selected_item,
    }
