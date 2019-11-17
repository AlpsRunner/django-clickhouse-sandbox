from django.core.management import BaseCommand
from infi.clickhouse_orm.database import Database

from dataclick.settings import CLICKHOUSE_DB_URL, CLICKHOUSE_DB_USERNAME, CLICKHOUSE_DB_PASS, CLICKHOUSE_DB_NAME


class Command(BaseCommand):
    def handle(self, *args, **options):
        db = Database(CLICKHOUSE_DB_NAME, db_url=CLICKHOUSE_DB_URL, username=CLICKHOUSE_DB_USERNAME,
                      password=CLICKHOUSE_DB_PASS)
        db.migrate('analyzeapp.clickhouse_migrations')
