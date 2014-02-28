from django.db import models
from django_semantic_mediawiki.models import WikiModel, WikiCharField

from datetime import datetime
import pytz


class Event(WikiModel):

    name = WikiCharField()
    url = models.URLField()
    place = WikiCharField(db_column='place')
    last_modified = models.DateTimeField(db_column='Modification date')
    event_date = models.DateTimeField(db_column='Date')
    status = WikiCharField(db_column='Event status')
    organizers = WikiCharField(db_column='Organizer')
    tags = WikiCharField(db_column='Tags')

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.place = self.place[0] if len(self.place) > 0 else ''
        self.status = self.status[0] if len(self.status) > 0 else None
        self.event_date = self.event_date[0] if len(self.event_date) > 0 else None

        if not self.event_date is None:
            self.event_date = datetime.utcfromtimestamp(float(int(self.event_date))).replace(tzinfo=pytz.timezone("Europe/Brussels"))

    def __unicode__(self):
        return self.name
