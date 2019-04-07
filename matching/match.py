from bintrees import FastRBTree

buy_orders = FastRBTree()
sell_orders = FastRBTree()

BUY = False
SELL = True



class Order:

	__init__(user, price, size, direction):
		self.time = __TIMESTAMP__
		self.user = user
		self.price = price
		self.size = size
		self.direction = direction


class ContractRequest:

	__init__(buyer, seller, price, size):
		self.buyer = buyer
		self.seller = seller
		self.price = price
		self.size = size

		send():
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
			)