import json
import pika
from notifications.channels import BaseNotificationChannel


class Producer(BaseNotificationChannel):
    """
    Fanout notifications for rabbitmq
    """

    def _connect(self):
        """
        Connecting to the rabbitmq server
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        return connection, channel

    def construct_message(self):
        """
        construct the message to be sent
        """
        extra_data = self.notification_kwargs['extra_data']

        return json.dumps(extra_data['message'])

    def notify(self, message):
        """
        put the message of the rabbitmq queue
        """
        connection, channel = self._connect()
        uri = self.notification_kwargs['extra_data']['uri']
        channel.exchange_declare(exchange=uri, exchange_type='fanout')
        channel.basic_publish(exchange=uri, routing_key='', body=message)

        connection.close()
