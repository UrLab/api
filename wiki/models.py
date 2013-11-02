from django.db import models
from wikiapi.models import WikiModel, WikiCharField

class Event(WikiModel):

    name = WikiCharField()
    url = models.URLField()
    place = WikiCharField(db_column='place')
    last_modified = models.DateTimeField(db_column='Modification date')
    event_date = models.DateTimeField(db_column='Date')
    status = WikiCharField(db_column='Event status')
    organizer = WikiCharField(db_column='Organizer')
    tags = WikiCharField(db_column='Tags')

    def __unicode__(self):
        return self.name
