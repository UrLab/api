from datetime import datetime
from time import mktime
import puka
import simplejson as json
from meteo.models import Temperature, Light

def ISOtime2JStstamp(timestr):
    time = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S.%f')
    return 1000*mktime(time.timetuple())

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    SERVER = "amqp://localhost/"
    QUEUE = "api.meteo.feed"
    help = """Feed weather data"""

    def log(self, msg):
        self.stdout.write("[%s] %s"%(str(datetime.now()), msg))

    def handle(self, *args, **options):
        self.client = puka.Client(self.SERVER)

        try:
            promise = self.client.connect()
            self.client.wait(promise)
            self.log("Connected to %s"%(self.SERVER))

            promise = self.client.queue_declare(queue=self.QUEUE)
            self.client.wait(promise)
            self.log("Got queue %s"%(self.QUEUE))

            promise = self.client.basic_consume(queue=self.QUEUE, prefetch_count=1)
            while True:
                result = self.client.wait(promise)
                try:
                    data = json.loads(result["body"])
                    time = ISOtime2JStstamp(data['time'])
                    if 'light' in data:
                        Light.objects.create(
                            ltstamp=time,
                            inside=data['light']['inside'],
                            outside=data['light']['outside']
                        )
                        self.log('Received Light')
                    if 'temperature' in data:
                        Temperature.objects.create(
                            ttstamp=time,
                            ambiant=data['temperature']['ambiant'],
                            radiator=data['temperature']['radiator']
                        )
                        self.log('Received Temperature')
                except ValueError as err:
                    self.log("Malformed message '{body}\nExecption is {err}'".format(body=result["body"], err=err))
                except Exception as err:
                    self.log('%s: %s'%(err.__class__, err))

                self.client.basic_ack(result)

        except Exception as err:
            print err
        except KeyboardInterrupt: 
            self.log("Killed")

        promise = self.client.close()
        self.client.wait(promise)

        self.log("Goodbye")
