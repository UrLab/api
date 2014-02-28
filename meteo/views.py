# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
import simplejson as json
from datetime import datetime, timedelta

from .utils import ISOtime2JStstamp, datetime2JStstamp
from .models import Light, Temperature
from chartit import DataPool, Chart

#http://www.colourlovers.com/palette/3110687/Sunny_day
color = {
    'light': '#a1802b',
    'light2': '#dcab43',
    'temp2': '#b10804',
    'temp': '#3f3902',
}

def today(request):
    now = datetime.now()
    url = reverse('weather')+'?from='+str(now-timedelta(1))+'&to='+str(now)
    return redirect(url)

def thisweek(request):
    now = datetime.now()
    url = reverse('weather')+'?from='+str(now-timedelta(7))+'&to='+str(now)
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
        	'options': {
                'type': 'spline', 
                'stacking': False, 
                'color': color['light'],
                'yAxis': 0
            },
            'terms': {'ltstamp': ['inside']}
        },
        {
            'options': {
                'type': 'spline', 
                'stacking': False, 
                'color': color['light2'], 
                'yAxis': 0
            },
            'terms': {'ltstamp': ['outside']}
        },
        {
        	'options': {
                'type': 'spline', 
                'stacking': False,
                'color': color['temp'],
                'yAxis': 1
            },
            'terms':{'ttstamp': ['ambiant']}
        },
        {
            'options': {
                'type': 'spline', 
                'stacking': False,
                'color': color['temp2'],
                'yAxis': 1
            },
            'terms':{'ttstamp': ['radiator']}
        }],
        chart_options = {
            'chart': {'type': 'spline'},
        	'title': {'text': 'Light & Temperature'},
            'tooltip': {'shared': True},
            'xAxis': {
            	'title': {'text': 'Timestamp'}, 
            	'type': 'datetime',
            	'minTickInterval': 10
            },
            'yAxis': [
                {
                    'title' : {'text': "Light", 'style': {'color': color['light']}},
                    'labels': {'format': '{value}%','style': {'color': color['light']}}
                },
    			{
                    'opposite': True, 
                    'title': {'text': "Temperature", 'style': {'color': color['temp']}},
                    'labels': {'format': '{value}°C','style': {'color': color['temp']}}
                }
  			],
            'plotOptions': {
                'spline': {
                    'lineWidth': 2, 
                    'states': {'hover': {'lineWidth': 4}},
                    'marker': {'enabled': False}
                },
            }
        }
    )

    last_light = Light.objects.all().order_by('-ltstamp')[0]
    last_temp = Temperature.objects.all().order_by('-ttstamp')[0]

    #Step 3: Send the chart object to the template.
    return render_to_response('graf.html', {
        'weatherchart': cht,
        'light': last_light, 'temp': last_temp
    })