import logging

from dataclick.celery import app
from dataclick.settings import LOGGING_LEVEL, LOGGING_FILENAME, LOGGING_DATEFMT
from tasksapp.faker import Faker

logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_FILENAME, datefmt=LOGGING_DATEFMT)


@app.task
def simulate_user_activity(events_to_create=50):
    Faker.events_per_day_min = 50
    Faker.events_per_day_max = 200
    faker = Faker()
    faker_event = faker.events_creator()
    try:
        for _ in range(events_to_create):
            faker_event()
    except Exception as e:
        logging.WARNING(f'simulate_user_activity: {e}')
        events_to_create = 0
    return f'{events_to_create} users do something'
