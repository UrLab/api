import puka
import json
from meteo.config import AMQ_SERVER, AMQ_QUEUE

def on_connection(promise, result):
	print " [*] Connected"
	print " [-] Declaring queue %s..."%(AMQ_QUEUE)
	client.queue_declare(queue=AMQ_QUEUE, callback=on_queue_declare)

def on_queue_declare(promise, result):
	print " [*] Got queue %s"%(AMQ_QUEUE)
	msg = {
		'time': '2013-08-22 13:27:58.123456',
		'light': {
			'inside': 24.13,
			'outside': 74.9
		},
		'temp' : {
			'radiator': 14.9,
			'ambiant': 18.2
		}
	}
	print " [-] Sending message %s..."%(str(msg))
	client.basic_publish(
		exchange='',
		routing_key=AMQ_QUEUE,
		body=json.dumps(msg),
		callback=on_basic_publish
	)

def on_basic_publish(promise, result):
	print " [*] Message sent"
	client.loop_break()

client = puka.Client(AMQ_SERVER)
print " [-] Establishing connection to %s..."%(AMQ_SERVER)
client.connect(callback=on_connection)
client.loop()