import logging
import os
from random import randint, choice

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataclick.settings')

import django

django.setup()

from infi.clickhouse_orm.database import Database

from dataclick.settings import LOGGING_LEVEL, LOGGING_FILENAME, CLICKHOUSE_DB_URL, CLICKHOUSE_DB_USERNAME, \
    CLICKHOUSE_DB_PASS, LOGGING_DATEFMT, CLICKHOUSE_DB_NAME
from analyzeapp.clickhouse_models import DataclickStat
from tasksapp.models import Event

logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_FILENAME, datefmt=LOGGING_DATEFMT)


class ClickHouseActions:
    db = Database(CLICKHOUSE_DB_NAME, db_url=CLICKHOUSE_DB_URL, username=CLICKHOUSE_DB_USERNAME,
                  password=CLICKHOUSE_DB_PASS)
    event_record_schema = {
        'time': 'time',
        'user_id': 'user_id',
        'join_date': 'join_date',
        'registration_date': 'registration_date',
        'name': 'name',
        'email': 'email',
        'is_guest': 'is_guest',
        'target_id': 'step_id',
        'action_id': 'action_id',
        'id': 'event_id',
    }
    sended_chunk_size = 999  # because sqlite test DB restrictions
    to_send__events_id__chunk = None

    def __init__(self, simulate_drops=True):
        self.to_send__events_id = []
        self.simulate_drops = simulate_drops

    def get_record_from_orm(self, orm_obj):
        """
        Adapter for ClickHouse DB
        """
        event_record = {val: getattr(orm_obj, key) for key, val in self.event_record_schema.items()
                        if hasattr(orm_obj, key)}
        event_record.update({val: getattr(orm_obj.user, key) for key, val in self.event_record_schema.items()
                             if hasattr(orm_obj.user, key) and getattr(orm_obj.user, key) is not None \
                             and val not in event_record.keys()})
        return event_record

    def gather_data(self, limit=None):
        """
        Gathers not sended data and creates list of ClickHouse Objects in memory
        """
        if DataclickStat.objects_in(self.db).count():
            last_sended_record = DataclickStat.objects_in(self.db).order_by('-event_id')[0]
            self.to_send__events_id.extend(
                Event.objects.filter(pk__gt=last_sended_record.event_id).values_list('pk', flat=True))
        else:
            self.to_send__events_id.extend(Event.objects.all().values_list('pk', flat=True))
        if limit:
            self.to_send__events_id = self.to_send__events_id[:limit]
        logging.info(f'will be send to ClickHouse {len(self.to_send__events_id)} records')

    def send_data(self):
        """
        Sends all data in list of ClickHouse Objects to ClickHouse DB
        """
        counter = 0
        if self.to_send__events_id:
            for i in range(0, len(self.to_send__events_id), self.sended_chunk_size):
                self.to_send__events_id__chunk = self.to_send__events_id[i:i + self.sended_chunk_size]
                _counter = len(self.to_send__events_id__chunk)
                self.send_chunck()
                counter += _counter
            logging.info(f'sended to ClickHouse {counter} records')
        else:
            logging.info(f'nothing to send to ClickHouse')
        return counter

    def send_chunck(self):
        """
        Sends to ClickHouse chunck of data in list of ClickHouse Objects to be sended
        """
        events = Event.objects.filter(
            pk__in=self.to_send__events_id__chunk
        ).select_related('user')
        dataclickstat_objs = []
        for event in events:
            dataclickstat_objs.append(DataclickStat(**self.get_record_from_orm(event)))
        dropped_events = []
        if self.simulate_drops:
            for _ in range(randint(0, 15)):
                if dataclickstat_objs:
                    dropped_event = choice(dataclickstat_objs)
                    dropped_events.append(dropped_event)
                    dataclickstat_objs.remove(dropped_event)
        logging.info(f'to send in chunk: {len(self.to_send__events_id__chunk)}, dropped {len(dropped_events)}')
        self.db.insert(dataclickstat_objs)
        self.check_sended_chunk()
        if self.to_send__events_id__chunk:
            logging.info(f'to repeat after check: {len(self.to_send__events_id__chunk)}')
            self.send_chunck()
        else:
            logging.info(f'chunk sended successfully')

    def check_sended_chunk(self):
        """
        Check if chunk sends completely
        """
        to_send__event_id = set(self.to_send__events_id__chunk)
        clickhouse_records = DataclickStat.objects_in(self.db).filter(
            event_id__in=list(to_send__event_id)
        ).only('event_id')
        sended__event_id = set([el.event_id for el in clickhouse_records])
        self.to_send__events_id__chunk = list(to_send__event_id - sended__event_id)

    def load_data(self):
        """
        Loads all data from ClickHouse DB
        """
        clickhouse_records = DataclickStat.objects_in(self.db)
        logging.info(f'found in ClickHouse {clickhouse_records.count()} records')
        return clickhouse_records.count()

    def get_active_users_count_by_days(self):
        """
        Returns generator of unique active users COUNT by days
        """
        return self.db.select(
            "SELECT time, uniq(user_id) as active_users_count "
            "FROM dataclickstat "
            "GROUP BY time "
            "ORDER BY time"
        )

    def get_active_users_by_days(self):
        """
        Returns generator of unique active users by days
        """
        return self.db.select(
            "SELECT time, groupUniqArray(user_id) as active_users "
            "FROM dataclickstat "
            "GROUP BY time "
            "ORDER BY time"
        )
