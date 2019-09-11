import os
import urllib.parse

from peewee import SqliteDatabase, Model, IntegerField, DoubleField, DateTimeField,\
    CharField, TextField, PostgresqlDatabase

from datetime import datetime

import config

if os.environ.get("DATABASE_URL"):
    url = urllib.parse.urlparse(os.environ.get("DATABASE_URL"))
    db = PostgresqlDatabase(host=url.hostname, user=url.username, password=url.password, port=url.port,
                            database=url.path[1:])
else:
    db = SqliteDatabase(config.DB_NAME)


class _Model(Model):
    class Meta:
        database = db

    def json(self):
        return self.__data__


class XRate(_Model):
    class Meta:
        db_table = "xrates"
        indexes = (
            (("from_currency", "to_currency"), True),
        )

    from_currency = IntegerField()
    to_currency = IntegerField()
    rate = DoubleField()
    updated = DateTimeField(default=datetime.now)
    module = CharField(max_length=100)

    def __str__(self):
        return "XRate(%s=>%s): %s" % (self.from_currency, self.to_currency, self.rate)


class ApiLog(_Model):
    class Meta:
        db_table = "api_logs"

    request_url = CharField()
    request_data = TextField(null=True)
    request_method = CharField(max_length=100)
    request_headers = TextField(null=True)
    response_text = TextField(null=True)
    created = DateTimeField(index=True, default=datetime.now)
    finished = DateTimeField()
    error = TextField(null=True)


class ErrorLog(_Model):
    class Meta:
        db_table = "error_logs"

    request_data = TextField(null=True)
    request_url = TextField()
    request_method = CharField(max_length=100)
    error = TextField()
    traceback = TextField(null=True)
    created = DateTimeField(default=datetime.now, index=True)


def start_db():

    if not XRate.table_exists():

        XRate.create_table()
        XRate.create(from_currency=840, to_currency=980, rate=1, module="privat_api")
        XRate.create(from_currency=840, to_currency=643, rate=1, module="cbr_api")
        XRate.create(from_currency=1000, to_currency=840, rate=1, module="privat_api")
        XRate.create(from_currency=1000, to_currency=980, rate=1, module="cryptonator_api")
        XRate.create(from_currency=1000, to_currency=643, rate=1, module="cryptonator_api")

        for m in (ApiLog, ErrorLog):
            m.create_table()

    print("db created!")
