# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
import simplejson as json

from .models import Light, Temperature
from chartit import DataPool, Chart

def view_weather(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = DataPool(
        series=[{
        	'options': {'source': Light.objects.all()},
            'terms': ['ltstamp', 'inside', 'outside']
        },
        {
        	'options': {'source': Temperature.objects.all()},
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
    			{'title' : {'text': "Light (%)"}},
    			{'opposite': True, 'title': {'text': "Temperature (°C)"}}
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