from django.shortcuts import render

from analyzeapp.clickhouse_actions import ClickHouseActions
from tasksapp.models import Event


def index(request):
    events = Event.objects.all()
    clickhouseaction = ClickHouseActions()
    clickhouseaction_count = clickhouseaction.load_data()
    context = {
        'page_title': 'анализ данных',
        'events_count': events.count(),
        'clickhouseaction_count': clickhouseaction_count,
    }
    return render(request, 'analyzeapp/index.html', context=context)
