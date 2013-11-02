from wiki.models import Event
from rest_framework import serializers




class ListField(serializers.Field):
    def field_to_native(self, obj, field_name):
        """
        Serialize the object's class name.
        """
        if not obj is None:
        	return getattr(obj, self.source)

class UserSerializer(serializers.ModelSerializer):
    organizers = ListField(source='organizers')

    class Meta:
        model = Event
        fields = ('url', 'name', 'place', 'event_date', 'status', 'organizers')