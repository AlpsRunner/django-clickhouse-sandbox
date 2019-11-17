from django.db import models


class Users(models.Model):
    join_date = models.DateField(verbose_name='date joined', null=True)
    registration_date = models.DateField(verbose_name='date registered', null=True)
    name = models.CharField(verbose_name='user name', max_length=128)
    email = models.EmailField(verbose_name='user email')
    is_guest = models.BooleanField(verbose_name='is guest user')

    @property
    def join_date_as_str(self):
        return self.join_date.strftime('%d-%m-%Y') if self.join_date else '00-00-0000'

    @property
    def registration_date_as_str(self):
        return self.registration_date.strftime('%d-%m-%Y') if self.registration_date else '00-00-0000'


class Task(models.Model):
    pass


class Event(models.Model):
    SEE_TASK = 0
    TRY_SOLVE_TASK = 1
    SOLVE_TASK = 2

    ACTION_CHOICES = (
        (SEE_TASK, 'see the task'),
        (TRY_SOLVE_TASK, 'make solve submit (try to solve the task)'),
        (SOLVE_TASK, 'solve the task'),
    )

    time = models.DateField(verbose_name='date registered')
    action_id = models.CharField(verbose_name='user action', max_length=1,
                                 choices=ACTION_CHOICES)

    target = models.ForeignKey(Task, verbose_name='solving task', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, verbose_name='solver', on_delete=models.CASCADE)

    @property
    def time_as_str(self):
        return self.time.strftime('%d-%m-%Y') if self.time else '00-00-0000'

    class Meta:
        ordering = ['pk']
