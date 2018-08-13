from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files import File
from django_rq import job

from modules.report.models import Report
from modules.test_plans.models import Plan


@job
def create_report(name, user):
    with File(open('{}.txt'.format(name), 'w+')) as f:
        f.write(str(list(Plan.objects.values())))
        report = Report.objects.create(name=name, report_file=f, create_by=user)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('channel_report_{}'.format(user.pk), {"type": "chat_message",
                                                                                      "id": report.pk,
                                                                                      "name": name,
                                                                                      'file': report.report_file.url,
                                                                                      "create_at": str(
                                                                                          report.create_at)})
        return report
