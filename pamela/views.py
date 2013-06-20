from django.http import HttpResponse
from pamela.models import Stat, UserNames
import json


def getJson(request):
    info = {}
    info["UserNames"] = [name.name for name in UserNames.objects.all()]

    NbOfPoeple = Stat.objects.all().order_by('-time')
    info["NbOfPoeple"] = 0
    if len(NbOfPoeple) > 0:
        info["NbOfPoeple"] = NbOfPoeple[0].nbComputerUp

    return HttpResponse(json.dumps(info))
