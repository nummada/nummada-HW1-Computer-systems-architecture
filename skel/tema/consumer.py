"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import itertools
from tema.product import Coffee, Tea
from threading import Thread
import time

TYPE = "type"
PRODUCT = "product"
QUANTITY = "quantity"
ADD = "add"
REMOVE = "remove"

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self=self, kwargs=kwargs, name=kwargs['name'])
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time


    def add_product(self, product, cart_id, quantity):
        for _ in range(quantity):
            while not self.marketplace.add_to_cart(cart_id, product):
                time.sleep(self.retry_wait_time)

    def remove_product(self, product, cart_id, quantity):
        for _ in range(quantity):
            while not self.marketplace.remove_from_cart(cart_id, product):
                time.sleep(self.retry_wait_time)

    def make_actions(self, products, quantities, commands, cart_id):
        for i in range (len(products)):
            if commands[i] == ADD:
                self.add_product(products[i], cart_id, quantities[i])
            elif commands[i] == REMOVE:
                self.remove_product(products[i], cart_id, quantities[i])

    def run(self):

        cart_id = self.marketplace.new_cart()

        products = []
        quantities = []
        commands = []

        for list_aux in self.carts:
            for dict_aux in list_aux:
                command_type = dict_aux[TYPE]
                commands.append(command_type)
                product = dict_aux[PRODUCT]
                quantities.append(dict_aux[QUANTITY])
                products.append(product)
        
        self.make_actions(products, quantities, commands, cart_id)
        
        products_list = self.marketplace.place_order(cart_id)

        products_list = products_list[::-1]
        for product in products_list:
            print(self.name + " bought " + repr(product[0]))