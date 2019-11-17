from django.core.management import BaseCommand

from analyzeapp.clickhouse_actions import ClickHouseActions


class Command(BaseCommand):
    def handle(self, *args, **options):
        clickhouseaction = ClickHouseActions()
        print('Active users ID by days:')
        [print(f'\t{el.time}:\n\t\t{", ".join(map(str, el.active_users))}')
         for el in clickhouseaction.get_active_users_by_days()]
