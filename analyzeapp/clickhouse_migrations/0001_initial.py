from infi.clickhouse_orm import migrations
from analyzeapp import clickhouse_models

operations = [
    migrations.CreateTable(clickhouse_models.DataclickStat),
]
