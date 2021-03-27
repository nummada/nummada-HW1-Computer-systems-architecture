"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
import time
# from tema.product import Coffee, Tea

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
        self.products = []
        self.quantities = []
        self.commands = []


    def add_product(self, product, cart_id, quantity):
        """adds a product in the cart"""
        for _ in range(quantity):
            while not self.marketplace.add_to_cart(cart_id, product):
                time.sleep(self.retry_wait_time)

    def remove_product(self, product, cart_id, quantity):
        """removes a product from the cart"""
        for _ in range(quantity):
            while not self.marketplace.remove_from_cart(cart_id, product):
                time.sleep(self.retry_wait_time)

    def make_actions(self, products, quantities, commands, cart_id):
        """make the add or remove actions"""
        for i, product in enumerate (products):
            if commands[i] == ADD:
                self.add_product(product, cart_id, quantities[i])
            elif commands[i] == REMOVE:
                self.remove_product(product, cart_id, quantities[i])

    def init_data(self, dictionary):
        """create data structures that hold the program input"""
        command_type = dictionary[TYPE]
        self.commands.append(command_type)
        self.quantities.append(dictionary[QUANTITY])
        product = dictionary[PRODUCT]
        self.products.append(product)

    def run(self):

        cart_id = self.marketplace.new_cart()

        for sublist in self.carts:
            for dictionary in sublist:
                self.init_data(dictionary)

        self.make_actions(self.products, self.quantities, self.commands, cart_id)

        products_list = self.marketplace.place_order(cart_id)

        products_list.reverse()
        for product in products_list:
            print(self.name + " bought " + repr(product[0]))
