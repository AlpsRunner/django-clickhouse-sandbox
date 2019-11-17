from infi.clickhouse_orm import migrations
from analyzeapp import clickhouse_models

operations = [
    migrations.AlterTable(clickhouse_models.DataclickStat),
]
