from django.core.management import BaseCommand

from tasksapp.faker import Faker


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        faker.create_users(quantity=1000)
        faker.create_tasks(quantity=250)
