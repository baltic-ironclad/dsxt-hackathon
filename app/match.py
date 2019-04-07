import time

buy_orders, sell_orders = [], []

BUY = False
SELL = True


class Order:
    def __init__(self, user, price, size, direction):
        self.time = time.time()
        self.user = user
        self.price = price
        self.size = size
        self.direction = direction

    def __str__(self):
        return "{}, {}, {}".format(self.user, self.price, self.size)

    def __lt__(self, other):
        if self.price < other.price:
            return True
        elif self.price > other.price:
            return False
        elif self.time < other.time:
            return True
        else:
            return False


class ContractRequest:
    def __init__(self, order1, order2, size):
        if order1.direction == BUY:
            self.buyer, self.seller = order1, order2
        else:
            self.buyer, self.seller = order2, order1
        self.price = self.seller.price
        self.size = size

    def __str__(self):
        return "{}, {}, {}, {}".format(self.buyer.user, self.seller.user,
                                       self.price, self.size)


def match_orders(order1, order2):
    if order1.direction == BUY:
        buyer, seller = order1, order2
    else:
        buyer, seller = order2, order1

    return seller.price <= buyer.price


def handle_new_order(new_order):
    if new_order.direction == BUY:
        if len(buy_orders) != 0 and new_order.price <= max(buy_orders).price:
            buy_orders.append(new_order)
            return
        orders_list1 = buy_orders
        orders_list2 = sell_orders

    else:
        if len(sell_orders) != 0 and new_order.price >= min(sell_orders).price:
            sell_orders.append(new_order)
            return
        orders_list1 = sell_orders
        orders_list2 = buy_orders

    executed = False

    while len(orders_list2) > 0:
        order = min(orders_list2) if new_order.direction == BUY else max(orders_list2)
        if match_orders(new_order, order):

            dealSize = min(new_order.size, order.size)
            print("dealsize:", dealSize, new_order.size, order.size)

            request = ContractRequest(new_order, order, dealSize)
            print(request)

            new_order.size -= dealSize
            order.size -= dealSize

            if new_order.size == 0:
                executed = True
                if order.size == 0:
                    orders_list2.remove(order)
                break
            orders_list2.remove(order)
        else:
            break

    if not executed:
        orders_list1.append(new_order)
