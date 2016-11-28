import os
import playhouse.db_url

from peewee import *

database = playhouse.db_url.connect(os.getenv("DATABASE", "sqlite:///app.db"))

class BaseModel(Model):
    class Meta:
        database = database
