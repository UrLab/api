from django.db import models
from wikiapi.models import WikiModel

class Event(WikiModel):

    name = models.CharField()
    url = models.URLField()
    place = models.CharField(db_column='place')
    last_modified = models.DateTimeField(db_column='Modification date')
    event_date = models.DateTimeField(db_column='Date')
    status = models.CharField(db_column='Event status')
    organizer = models.CharField(db_column='Organizer')
    tags = models.CharField(db_column='Tags')

    def __unicode__(self):
        return self.name
