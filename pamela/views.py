from django.http import HttpResponse
from pamela.models import Stat, UserNames
import json

def get(request):
	info = {}
	info["UserNames"] = [name.name for name in UserNames.objects.all()]
	info["NbOfPoeple"] = Stat.objects.all().order_by('time')[0].nbComputerUp
	return HttpResponse(json.dumps(info))

