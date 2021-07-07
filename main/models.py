from django.db.models import *


class Interval(Model):
    buy = FloatField()
    sell = FloatField()
    date = DateField()
    time = TimeField()
    unix = IntegerField()


class Check(Model):
    buy = FloatField()
    sell = FloatField()
    date = DateField()
    time = TimeField()
    unix = IntegerField()


class Config(Model):
    API = CharField(max_length=46)
    TAPI = CharField(max_length=46)
    interval = IntegerField()
    check = IntegerField()
    jalgas = IntegerField()
    galymjan = IntegerField()
    iteration = IntegerField()
    banks = CharField(max_length=200)
    bot = BooleanField()
    gmail = BooleanField()
    porog_interval = IntegerField()
    porog_check = IntegerField()
    json = IntegerField()


class Change(Model):
    buy = FloatField()
    sell = FloatField()
    dfbp = FloatField()
    dfsp = FloatField()
    dfbtg = FloatField()
    dfstg = FloatField()
    date = DateField()
    time = TimeField()
    unix = IntegerField()
    big = BooleanField()