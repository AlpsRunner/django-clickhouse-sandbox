import datetime
import logging
from random import choice, randint

from django.db.models import Max

from dataclick.settings import LOGGING_LEVEL, LOGGING_FILENAME, LOGGING_DATEFMT
from tasksapp.models import Users, Task, Event

logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_FILENAME, datefmt=LOGGING_DATEFMT)


class Faker:
    current_event_day = None
    day_event_counter = None
    events_per_day = None
    events_per_day_min = 150
    events_per_day_max = 500

    @staticmethod
    def random_date(start_year=2017, end_year=2019):
        return datetime.date(
            year=randint(start_year, end_year),
            month=randint(1, 12),
            day=randint(1, 28),
        )

    @staticmethod
    def random_name(name_length=10, start_letter='a', end_letter='z'):
        return ''.join([chr(randint(ord(start_letter), ord(end_letter))) for _ in range(name_length)])

    def create_users(self, quantity=50):
        users = []
        for _ in range(quantity):
            join_date = None
            registration_date = None
            is_guest = bool(randint(0, 1))
            if not is_guest:
                join_date = self.random_date()
                registration_date = self.random_date()
                while not 0 <= (registration_date - join_date).days <= 30:
                    registration_date = self.random_date()

            name = self.random_name(randint(3, 15), 'а', 'я').title()
            email = f'{self.random_name(randint(4, 15))}@{self.random_name(randint(2, 15))}.' \
                    f'{self.random_name(randint(2, 3))}'

            logging.info(f' {join_date}, {registration_date}, {name}, {email}, {is_guest}')
            users.append(Users(join_date=join_date, registration_date=registration_date, name=name,
                               email=email, is_guest=is_guest))
        Users.objects.bulk_create(users)

    def create_tasks(self, quantity=100):
        tasks = []
        for _ in range(quantity):
            tasks.append(Task())
        Task.objects.bulk_create(tasks)

    @classmethod
    def set_events_per_day(cls):
        cls.events_per_day = randint(cls.events_per_day_min, cls.events_per_day_max)

    @classmethod
    def events_creator(cls):
        users = list(Users.objects.all())
        tasks = list(Task.objects.all())
        if not cls.current_event_day:
            cls.current_event_day = Event.objects.aggregate(Max('time'))['time__max']
            if not cls.current_event_day:
                cls.current_event_day = datetime.date.today()
        if not cls.day_event_counter:
            cls.day_event_counter = 0
            cls.set_events_per_day()

        def create_event():
            user = choice(users)
            task = choice(tasks)
            action_id = choice(Event.ACTION_CHOICES)[0]
            if cls.day_event_counter == cls.events_per_day:
                cls.current_event_day += datetime.timedelta(days=1)
                cls.day_event_counter = 0
                cls.set_events_per_day()
            time = cls.current_event_day
            cls.day_event_counter += 1
            # logging.info(f' {time}, {action_id}, {task}, {user}')
            return Event.objects.create(time=time, action_id=action_id, target=task, user=user)

        return create_event
