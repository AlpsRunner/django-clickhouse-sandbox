from django.core.management import BaseCommand

from analyzeapp.clickhouse_actions import ClickHouseActions


class Command(BaseCommand):
    def handle(self, *args, **options):
        clickhouseaction = ClickHouseActions()
        print('Active users count by days:')
        [print(f'\t{el.time}: {el.active_users_count}') for el in clickhouseaction.get_active_users_count_by_days()]
