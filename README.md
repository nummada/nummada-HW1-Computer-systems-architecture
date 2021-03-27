
Name: Mihaela-Mădălina Nuță  
Group: 334CB

# Homework 1

>### Explications of the solution:

####  General approach:
* The general approach involves the usage of some simple synchronization mechanisms. The program has to simulate the solution for the problem "Multiple producers, multiple consumers".  The producers and consumers communicate with each other  with the help of an intermediate instance of the program: Marketplace. 
* The Marketplace manage all the operations that the producers and the consumer do, such as: publish (by the producers), add to / remove from cart (by the consumers).  

* **Producer:**
	+ is initiated with the ``daemon property`` of a thread so it will exit when the main program exits (that is, when consumers finish the execution)
	+ at the beginning, the producer register himself at the Marketstore and gets a __*producer id*__
	+ using the input, he starts to produce coffee or tea in a loop
	+ he has a delay while producing a single product
	+ when the Marketplace tells him that there is **no space left** in the store for him, he waits for a fixed amount of time and then try again
	+ he will have more space left in the store when a consumer will buy his product
	+ he will stop the execution when the consumers will stop the execution. **Explanation:** the producer thread is a *daemon thread*

* **Consumer:**
	+ is not a daemon thread, he will stop the execution by being waited by the main thread using __*join*__
	+ at the beginning, the consumer gets a cart (from the Marketplace)  represented by a **cart id**
	+ using the chosen data structures, he will store the input data containing the products and the cantity
	+ chosen data structures:
		* a list containing the quantities
		* a list of products
		* a list of commands (as ADD/REMOVE)
	+ he starts to add to / remove from the cart using the Marketplace's available functions
	+ when the consumer tries to *add to the cart* an **item** that is **not available** on the market, he waits for a fixed amount of time and then try again
	+ when the consumer tries to *remove from the cart* a product and in the Marketstore there is **no space left for that product**, he waits for a fixed amount of time and then try again. **UPDATE** - we will not wait, the marketplace will simply add that back, because the initial approach would end into a deadlock
	+ at the end, he place the order and gets the products from the Marketplace

* **Marketplace:**
	+ contains the available functions that the consumers or producers can use
	+ **register_producer**: when a producer register himself, the class uses a __*lock*__ . The producer is assigned to a queue containing his products and the queue receives a **lock**
	+ **publish**: when a producer tries to publish a product on the market, the marketplace uses a **lock**. This is required because the function uses the length of the producer's queue (not only the __append function__ that is ```thread safe```. If the queue is full, the marketplace will not keep the products and will tell the producer that there is **no space left** for him. Else, he will keep the product in the store
	+ **new_cart**: when a consumer wants a cart, the class will use a **lock** because the operations involve both length and append functions (that together are not thread safe)
	+ **add_to_cart:** when a consumer wants a product, the class will search for it. For every  producer's queue, he has a **lock**. He is made that way because it would be more expensive to use a global lock for all of the queues. The consumers would have to wait other consumers to add to the cart. If the products does not exist, the market would tell the consumer to wait and try again. When adding to the card, there is **no need of a lock** because there will be **only one costumer** that will add an item at that index
	+ The products are stored in the cart using a **tuple** containing the product and the index of the queue, because when the costumer tries to remove a product from the cart, the product have to be **put back in the same queue**
	+ **remove_from_cart:**  the marketplace will search for the product in the list of tuples and remove that products and then add that product back to the producer's queue represented by the index from the tuple
	+ chosen data structures:
		* a list of carts
		* a list of queues for producers
		* a list of locks for queues

> The homework helped to understand the basic synchronization mechanisms from Python and to manage better the language itself.

> The implementation is good enough. A good improvement is that the Marketplace uses a lock for every queue so that the costumers do not have to wait for each other to add to the cart. 


>###  Implementation
* All the functionalities of the project are implemented
* All the tests pass
* Encountered problems:
	* bad usage of the queues locks
	* at the beginning the Marketplace would not stop the searching for a product and the search would match multiple products 
* Interesting facts: ```daemon threads```