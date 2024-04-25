from django import template

register = template.Library()

@register.filter(name='toggle_category')
def toggle_category(category_str, category_id):
    if not category_str:
        return str(category_id)
    category_list = category_str.split(',')
    if str(category_id) in category_list:
        category_list.remove(str(category_id))
    else:
        category_list.append(str(category_id))
    out = ','.join(category_list)
    return out