# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import json
from mpd import MPDClient

class MpdClient:
    def __enter__(self):
        client = MPDClient(use_unicode=True)
        self.client = client
        client.timeout = 1
        client.idletimeout = None
        client.connect("131.urlab.be", 6600)
        return client
    def __exit__(self, type, value, traceback):
        self.client.close()
        self.client.disconnect()


def index(request):
    with MpdClient() as client:
        status = client.status()
        current = client.currentsong()

    # title, artiste, album, progression, status,
    ret = {
        'volume' : int(status['volume']),
        'shuffle': False if status['random'] == '0' else True,
        'repeat' : False if status['repeat'] == '0' else True,
        'progression' : float(status['elapsed']),
        'album' : current['album'],
        'artist' : current['artist'],
        'title' : current['title'],
        'file' : '/home/'+current['file'],

    }
    return HttpResponse(json.dumps(ret), mimetype='application/json')