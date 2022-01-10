# amqps://escodtac:q6ek_xlRp-9fcdUY_Y9EmORpJ7b1NI3a@toad.rmq.cloudamqp.com/escodtac
import pika, json

params = pika.URLParameters('amqps://escodtac:q6ek_xlRp-9fcdUY_Y9EmORpJ7b1NI3a@toad.rmq.cloudamqp.com/escodtac')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
