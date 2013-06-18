from django.core.management.base import BaseCommand, CommandError 
from pamela.models import Stat, UserNames
import redis, time

class Command(BaseCommand):
    args = "None"
    help = "Listend to a pamela redis server"

    def handle(self):
        r = redis.StrictRedis(host='192.168.1.11', port=6379, db=0)

        while True:
            wait = True
            username = r.get(username)
            if username != None:
                wait = False
                print "Username: "+username
            if wait:
                time.sleep(1)

