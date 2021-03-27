"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
# from tema.marketplace import Marketplace
import time

ID = 0
CANTITY = 1
PRODUCING_DELAY = 2

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self=self, name=kwargs['name'], daemon=kwargs['daemon'])
        self.producs = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def produce_single_product(self, producer_id, product):
        """produces a single product"""
        time.sleep(product[PRODUCING_DELAY])
        while not self.marketplace.publish(producer_id, product[ID]):
            time.sleep(self.republish_wait_time)

    def produce(self, producer_id):
        """produces all the products in a loop"""
        while True:
            for product in self.producs:
                for _ in range (0, product[CANTITY]):
                    self.produce_single_product(producer_id, product)

    def run(self):
        producer_id = self.marketplace.register_producer()
        self.produce(producer_id)
