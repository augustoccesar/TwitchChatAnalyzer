from peewee import Model, TextField, DoubleField

from twitchchatanalyzer.analyzer.database import DB


class BaseModel(Model):
    """ Base model to be extended by all other models.
    """
    class Meta:
        """ Meta definition to be extended by all models.
        """
        database = DB


class Message(BaseModel):
    """ Model representing the Twitch Message
    """
    username = TextField()
    text = TextField()
    time = DoubleField()
