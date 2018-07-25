from django import template
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import gettext as _

register = template.Library()


@register.simple_tag
def case_status(request):
    if request.user.is_authenticated:
        cases = request.user.case_set.all()
        for case in cases:
            try:
                logs = case.last_two_logs
                if logs[0].status != logs[1].status:
                    if logs[1].status == '1':
                        messages.add_message(request, messages.WARNING, format_html(
                            "{} <a href='{}' class='alert-warning-link font-weight-bold'> {}</a> {}".format(_("Кейс"), logs[1].case.get_absolute_url(), logs[1].case.name, _("закончился с ошибкой"))))
            except IndexError:
                pass
    return ""
