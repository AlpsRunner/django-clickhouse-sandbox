from django.core.management import BaseCommand
from infi.clickhouse_orm.database import Database

from analyzeapp.clickhouse_models import DataclickStat
from dataclick.settings import CLICKHOUSE_DB_URL, CLICKHOUSE_DB_USERNAME, CLICKHOUSE_DB_PASS


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = Database('dataclick_stat', db_url=CLICKHOUSE_DB_URL, username=CLICKHOUSE_DB_USERNAME,
                      password=CLICKHOUSE_DB_PASS)
        db.create_table(DataclickStat)
