from django import template
from users.models import Notification

register = template.Library()

@register.inclusion_tag('users/show_notifs.html', takes_context=True)
def show_notifs(context):
    request_user = context['request'].user
    notifs = Notification.objects.filter(to_user=request_user).exclude(notif_seen=True).order_by('-date')
    return {'notifs':notifs}


