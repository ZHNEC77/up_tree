from django import template
from django.template.context import RequestContext
from django.utils.safestring import SafeString

from tree_menu.models import Item


register = template.Library()


@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu: SafeString) -> dict:
    all_items = context.get('all_items', [])
    items = [item for item in all_items if item.menu.title == menu]

    items_by_id = {item.id: item for item in items}

    for item in items:
        item.child_items = []

    root_items = []
    for item in items:
        if item.parent_id:
            parent = items_by_id.get(item.parent_id)
            if parent:
                parent.child_items.append(item)
        else:
            root_items.append(item)

    selected_slug = context['request'].GET.get(menu)
    selected_item = None
    selected_path_ids = set()

    if selected_slug:
        selected_item = next(
            (item for item in items if item.slug == selected_slug), None)
        if selected_item:
            current = selected_item
            while current:
                selected_path_ids.add(current.id)
                current = items_by_id.get(current.parent_id)

    def mark_selected(items_list):
        for item in items_list:
            item.is_selected = item.id in selected_path_ids
            if hasattr(item, 'child_items'):
                mark_selected(item.child_items)

    mark_selected(root_items)

    result_dict = {
        'items': root_items,
        'menu': menu,
        'selected_item': selected_item,
    }

    return result_dict
