"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_produces = queue_size_per_producer
        self.carts_products = []
        self.producers_queues = []
        self.register_producer_lock = Lock()
        self.register_cart_lock = Lock()
        self.publish_lock = Lock()

        self.queues_locks = []

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.register_producer_lock.acquire()

        producer_id = len(self.producers_queues)
        self.producers_queues.append([])
        self.queues_locks.append(Lock())

        self.register_producer_lock.release()
        
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.publish_lock.acquire()

        if len(self.producers_queues[producer_id]) > self.queue_size_per_produces:
            self.publish_lock.release()
            return False

        self.producers_queues[producer_id].append(product)

        self.publish_lock.release()
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.register_cart_lock.acquire()

        cart_id = len(self.carts_products)
        self.carts_products.append([])
        self.register_cart_lock.release()
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for i in range(len(self.producers_queues)):
            queue = self.producers_queues[i]
            self.queues_locks[i].acquire()
            for queue_product in queue:
                if queue_product == product:
                    self.carts_products[cart_id].append((product, i))
                    queue.remove(queue_product)
                    self.queues_locks[i].release()
                    return True
        
            self.queues_locks[i].release()
        return False



    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        found = False
        for pair in self.carts_products[cart_id]:
            if pair[0] == product:
                self.queues_locks[pair[1]].acquire()
                self.producers_queues[pair[1]].append(product)
                found = True
                self.carts_products[cart_id].remove(pair)
                self.queues_locks[pair[1]].release()
                break

        return found

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts_products[cart_id]