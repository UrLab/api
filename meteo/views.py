# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
import simplejson as json
from datetime import datetime, timedelta

from .utils import ISOtime2JStstamp, datetime2JStstamp
from .models import Light, Temperature
from chartit import DataPool, Chart

def today(requet):
    now = datetime.now()
    url = reverse('weather')+'?from='+str(now-timedelta(1))+'&to='+str(now)
    return redirect(url)

def weather(request):
    filters = {}
    if 'from' in request.GET:
        filters['pk__gte'] = ISOtime2JStstamp(request.GET['from'])
    if 'to' in request.GET:
        filters['pk__lte'] = ISOtime2JStstamp(request.GET['to'])

    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = DataPool(
        series=[{
        	'options': {'source': Light.objects.filter(**filters)},
            'terms': ['ltstamp', 'inside', 'outside']
        },
        {
        	'options': {'source': Temperature.objects.filter(**filters)},
            'terms': ['ttstamp', 'ambiant', 'radiator']
        }]
    )

    #Step 2: Create the Chart object
    cht = Chart(
        datasource=weatherdata,
        series_options = [{
        	'options': {'type': 'line', 'stacking': False, 'yAxis': 0},
            'terms': {'ltstamp': ['inside', 'outside']}
        },
        {
        	'options': {'type': 'line', 'stacking': False, 'yAxis': 1},
            'terms':{'ttstamp': ['ambiant', 'radiator']}
        }],
        chart_options = {
        	'title': {'text': 'Light & Temperature'},
            'xAxis': {
            	'title': {'text': 'Timestamp'}, 
            	'type': 'datetime',
            	'minTickInterval': 10000
            },
            'yAxis': [
    			{'title' : {'text': "Light (%)"}, 'color': '#CC3'},
    			{'opposite': True, 'title': {'text': "Temperature (°C)"}, 'color': '#33C'}
  			]
        }
    )

    last_light = Light.objects.all().order_by('-ltstamp')[0]
    last_temp = Temperature.objects.all().order_by('-ttstamp')[0]

    #Step 3: Send the chart object to the template.
    return render_to_response('graf.html', {
        'weatherchart': cht,
        'light': last_light, 'temp': last_temp
    })