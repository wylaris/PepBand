from django import template

register = template.Library()

@register.filter(name='addcpt')
def addcpt(value, args):
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) == 3:
        return value.as_widget(attrs={'class': arg_list[0], 'placeholder':arg_list[1], 'type':arg_list[2]})
    else:
        return value.as_widget(attrs={'class': arg_list[0], 'placeholder': arg_list[1]})