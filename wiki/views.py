from wiki.models import Event
from rest_framework import viewsets
from wiki.serializers import UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    List events present on the wiki
    """
    queryset = Event.objects.all()
    serializer_class = UserSerializer