from bintrees import FastRBTree
import time

buy_orders = FastRBTree()
sell_orders = FastRBTree()

BUY = False
SELL = True



class Order:

	def __init__(self, user, price, size, direction):
		self.time = time.time()
		self.user = user
		self.price = price
		self.size = size
		self.direction = direction


class ContractRequest:

	def __init__(buyer, seller, price, size):
		self.buyer = buyer
		self.seller = seller
		self.price = price
		self.size = size

	def send():
			pass

def matchOrders(buyer, seller):
	if seller.price > buyer.price:
		return False
	else:
		return True

def handleNewOrder(new_order):
	if new_order.direction == BUY:
		if not buy_orders.is_empty() and new_order.price <= max(buy_orders).price:
			buy_orders.insert(new_order)
			return

		executed = False

		for index, order in enumerate(sell_orders):
			if matchOrders(new_order, order):
				dealSize = min(new_order.size, order.size)
				
				request = ContractRequest(new_order.user, 
					order.user, order.price, dealSize)

				request.send()

				new_order -= dealSize

				order -= dealSize

				if new_order.size == 0:
					executed = true
					if order.size == 0:
						sell_orders.pop()
				break
			else: 
				break

		if not executed:
			buy_orders.insert(new_order)
	else:
		if not sell_orders.is_empty() and new_order.price >= min(buy_orders).price:
			sell_orders.insert(new_order)
			return

		executed = False

		for index, order in enumerate(buy_orders):
			if matchOrders(order, new_order):
				dealSize = min(order.size, new_order.size)
				
				request = ContractRequest(order.user, 
					new_order.user, order.price, dealSize)

				request.send()

				new_order -= dealSize

				order -= dealSize

				if new_order.size == 0:
					executed = true
					if order.size == 0:
						sell_orders.pop()
				break
			else: 
				break

		if not executed:
			sell_orders.insert(new_order)

def print_tree(tree, name):
	print(name)
	for elem in tree:
		print(elem)

if __name__ == "__main__":
	order1 = Order(10, 1000, 1, False)
	order1 = Order(11, 1000, 3, True)
	time.sleep(2)
	order1 = Order(12, 900, 2, True)
	order1 = Order(14, 1000, 3, False) 

	handleNewOrder(order1)
	print_tree(buy_orders, "buy_orders")
	print_tree(sell_orders, "sell_orders")

	handleNewOrder(order2)
	print_tree(buy_orders, "buy_orders")
	print_tree(sell_orders, "sell_orders")
	
	handleNewOrder(order3)
	print_tree(buy_orders, "buy_orders")
	print_tree(sell_orders, "sell_orders")
	
	handleNewOrder(order4)
	print_tree(buy_orders, "buy_orders")
	print_tree(sell_orders, "sell_orders")
	
