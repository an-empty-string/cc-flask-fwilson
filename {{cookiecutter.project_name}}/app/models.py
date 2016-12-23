import os
import playhouse.db_url

from . import utils
from datetime import datetime
from peewee import *

database = playhouse.db_url.connect(os.getenv("DATABASE", "sqlite:///app.db"))

class BaseModel(Model):
    class Meta:
        database = database

class UserSession(BaseModel):
    token = CharField(64)
    user = CharField(128)
    valid = BooleanField(default=True)

UserSession.create_table(fail_silently=True)
