from peewee import *
import json
from pathlib import Path
from types import SimpleNamespace as Namespace


config_path = str(Path(__file__).parent.parent)


def json2object(filename):
    with open(filename) as f:
        data = f.read()
    data = json.loads(data, object_hook=lambda d: Namespace(**d))
    PG_SQL_LOCAL = {
        'database': data.db_name,
        'user': data.db_user,
        'password': data.db_password,
        'host': data.db_host,
        'port': data.db_port,
    }
    return PG_SQL_LOCAL


CONF = json2object(config_path + '/config.conf')

database = PostgresqlDatabase(
    CONF["database"],
    **{'host': CONF["host"],
       'user': CONF["user"],
       'password': CONF["password"],
       'autoconnect': True, 'port': CONF["port"],
       'connect_timeout': 300
       }
)


class BaseModel(Model):
    class Meta:
        database = database


class Testing(BaseModel):
    id = AutoField(primary_key=True, index=True)
    content = TextField()
    result = TextField(null=True, default="{}")
    user_id = IntegerField(null=False)

    class Meta:
        table_name = "testing"


class Functional(BaseModel):
    id = AutoField(primary_key=True, index=True)
    test = ForeignKeyField(Testing, on_delete="CASCADE")
    function = TextField()

    class Meta:
        table_name = "functional"


def create_table(table):
    if not table.table_exists():
        table.create_table()

create_table(Testing)
create_table(Functional)
