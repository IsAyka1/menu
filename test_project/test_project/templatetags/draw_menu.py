from django import template

from my_menu.models import Menu

register = template.Library()


# @register.inclusion_tag('menu.html')
# def draw_menu(value: str):
#     menu = Menu.objects.filter(name=value)[0]
#     return {
#         'menu': menu,
#         'selected_name': menu.name,
#         'before_selected': True,
#     }


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu: str | Menu):
    if isinstance(menu, str):
        try:
            menu = Menu.objects.filter(name=menu)[0]
        except IndexError:
            return {
                'to_draw': False
            }
    return {
        'menu': menu,
        'selected_name': context.get('selected_name', menu.name),
        'before_selected': context.get('before_selected', True),
        'to_draw': True,
        'parent_context': context,
    }


@register.simple_tag(takes_context=True)
def change_context(context, attr: str, new_val):
    context[attr] = new_val
    cur = context.get('parent_context', None)
    while cur is not None:
        context = cur
        context[attr] = new_val
        cur = context.get('parent_context', None)
    # print('get False', str(context[attr]))
    context[attr] = new_val
    return ''
