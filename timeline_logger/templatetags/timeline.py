from django.template import Library


register = Library()


@register.simple_tag
def render_message(log_entry, template=None, **context):
    return log_entry.get_message(template=template, **context)
