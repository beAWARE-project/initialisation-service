from confluent_kafka import Consumer
import bus.load_credentials
import json
import asyncio


import zonesGen.zones_creator as znGen


class BusConsumer:
    def __init__(self):

        # Pre-shared credentials
        # self.credentials = json.load(open('bus_credentials.json'))

        self.credentials = bus.load_credentials.LoadCredentials.load_bus_credentials()

        # Construct required configuration
        self.configuration = {
            'client.id': 'KB_consumer',
            'group.id': 'KB_consumer_group',
            'bootstrap.servers':  ','.join(self.credentials['kafka_brokers_sasl']),
            'security.protocol': 'SASL_SSL',
            'ssl.ca.location': '/etc/ssl/certs',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': self.credentials['api_key'][0:16],
            'sasl.password': self.credentials['api_key'][16:48],
            'api.version.request': True
        }

        self.consumer = Consumer(self.configuration)

        self.listening = True

        self.database = 'messages.sqlite'

    def listen(self, topics):
        # Topics should be a list of topic names e.g. ['topic1', 'topic2']

        self.listening = True

        # Subscribe to topics
        try:
            self.consumer.subscribe(topics)
        except Exception as e:
            print("Error @ BusConsumer.listen()")
            print(e)
            return False

        # Initiate a loop for continuous listening
        while self.listening:
            msg = self.consumer.poll(0)

            # If a message is received and it is not an error message
            if msg is not None and msg.error() is None:

                # Add incoming message to requests database
                try:
                    message_text = msg.value().decode('utf-8')
                except:
                    message_text = msg.value()

                self.submit_message_process(message_text)

        # Unsubscribe and close consumer
        self.consumer.unsubscribe()
        self.consumer.close()

    def stop(self):
        self.listening = False

    def submit_message_process(self, message):
        znGen.generateTopic()