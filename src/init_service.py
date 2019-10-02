#! python3
import threading
from bus.bus_consumer import BusConsumer


class ListenerThread(threading.Thread):
    def __init__(self, listen_to_topics):
        threading.Thread.__init__(self)

        self.listen_to_topics = listen_to_topics
        self.consumer = None

    def run(self):
        print("Initiated listener on topics", self.listen_to_topics)

        # Create consumer object
        self.consumer = BusConsumer()

        # Start listening to bus
        self.consumer.listen(self.topics)

    def stop(self):
        self.consumer.stop()

    def get_topics(self):
        return self.topics

def runListenThread():
	topics = [
        'TOP111_ZONES_INITIALIZATION'
    ]
    # Create new threads
    thread1 = ListenerThread(listen_to_topics=topics)

    # Start new Threads
    thread1.start()

    print("Exiting Main Thread")
    
if __name__ == "__main__":
    runListenThread()
