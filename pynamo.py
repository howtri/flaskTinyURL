from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
)


class User(Model):
    class Meta:
        table_name = 'tiny-table-users'
        region = 'us-east-1'

    username = UnicodeAttribute(hash_key=True)
    password = UnicodeSetAttribute()
    admin = BooleanAttribute()
    timeCreated = UTCDateTimeAttribute()


class Url(Model):
    class Meta:
        table_name = 'tiny-table'
        region = 'us-east-1'

    shortID = UnicodeAttribute(hash_key=True)
    longURL = UnicodeSetAttribute()
    timeCreated = UTCDateTimeAttribute()
    hits = NumberAttribute()
    lastHit = UTCDateTimeAttribute(null=True)
    creator = UnicodeSetAttribute()
