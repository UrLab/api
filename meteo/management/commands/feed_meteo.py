from datetime import datetime
import puka
import simplejson as json
from meteo.models import Temperature, Light
from meteo.utils import ISOtime2JStstamp
from django.core.management.base import BaseCommand
from meteo.config import AMQ_SERVER, AMQ_QUEUE

class Command(BaseCommand):
    help = """Feed weather data"""

    def log(self, msg):
        self.stdout.write("[%s] %s"%(str(datetime.now()), msg))

    def handle(self, *args, **options):
        self.client = puka.Client(AMQ_SERVER)

        try:
            promise = self.client.connect()
            self.client.wait(promise)
            self.log("Connected to %s"%(AMQ_SERVER))

            promise = self.client.queue_declare(queue=AMQ_QUEUE)
            self.client.wait(promise)
            self.log("Got queue %s"%(AMQ_QUEUE))

            promise = self.client.basic_consume(queue=AMQ_QUEUE, prefetch_count=1)
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
