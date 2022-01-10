import pika, json,  os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://escodtac:q6ek_xlRp-9fcdUY_Y9EmORpJ7b1NI3a@toad.rmq.cloudamqp.com/escodtac')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.like = product.like +1
    product.save()
    print('product likes increased')
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('Started Consuming')

channel.start_consuming()
channel.close()
