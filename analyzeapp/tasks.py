import logging

from analyzeapp.clickhouse_actions import ClickHouseActions
from dataclick.celery import app
from dataclick.settings import LOGGING_LEVEL, LOGGING_FILENAME, LOGGING_DATEFMT

logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_FILENAME, datefmt=LOGGING_DATEFMT)


@app.task
def gather_and_send_data():
    counter = 0
    clickhouseaction = ClickHouseActions(simulate_drops=True)
    try:
        clickhouseaction.gather_data(limit=None)
        counter = clickhouseaction.send_data()
    except Exception as e:
        logging.WARNING(f'gather_and_send_data: {e}')
    return f'{counter} records send successfully'
