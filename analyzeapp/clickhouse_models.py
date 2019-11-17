from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import DateField, UInt8Field, UInt16Field, UInt32Field, NullableField, StringField
from infi.clickhouse_orm.engines import Memory


class DataclickStat(Model):
    time = DateField()
    user_id = UInt32Field()
    join_date = NullableField(DateField())
    registration_date = NullableField(DateField())
    name = StringField()
    email = StringField()
    is_guest = UInt8Field()
    step_id = UInt32Field()
    action_id = UInt8Field()
    event_id = UInt32Field()

    engine = Memory()

    @property
    def time_as_str(self):
        return self.time.strftime('%d-%m-%Y') if self.time else '00-00-0000'

    @property
    def join_date_as_str(self):
        return self.join_date.strftime('%d-%m-%Y') if self.join_date else '00-00-0000'

    @property
    def registration_date_as_str(self):
        return self.registration_date.strftime('%d-%m-%Y') if self.registration_date else '00-00-0000'
