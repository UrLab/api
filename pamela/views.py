from django.http import HttpResponse
from pamela.models import Stat, UserNames

def get(request):
	info = {}
	info['userConnected'] = UserNames.objects.all().order_by('name')
	info['Stat'] = Stat.objects.all().order_by('time')
	return HttpResponse(str(info))

