from peewee import *
import os

db = PostgresqlDatabase('translator', user='postgres', password='secret', host='localhost', port=5432)


class Emoji():
    string = CharField()
    
    class Meta:
        database = db


def reboot():
    Emoji.delete().execute()


def check(s):
    for i in [ '&', ';', '$', '<', '>']:
        if i in s:
            return False
    return True


def add_new(emoji, text):
    if check(emoji) and check(text) :
        e, is_created = Emoji.get_or_create(string=emoji)
        if is_created:
            with open('./translations/%s' % emoji, 'w') as f:
                f.write(text)


def get_translations(sort_by):
    records = [{'emoji': x.string, 'text': os.popen('cat ./translations/%s' % x.string).read()} for x in Emoji.select()]
    records.sort(key=lambda x: len(x[sort_by]), reverse=True)
    return records

db.create_tables([Emoji])

