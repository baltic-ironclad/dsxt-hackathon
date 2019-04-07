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


class ContractRequest:
    def __init__(self, buyer, seller, price, size):
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.size = size

    def send(self):
        pass


def match_orders(order1, order2):
    if order1 == BUY:
        buyer = order1
        seller = order2
    else:
        buyer = order2
        seller = order1

    if seller.price > buyer.price:
        return False
    else:
        return True


def handle_new_order(new_order):
    if new_order.direction == BUY:
        if len(buy_orders) != 0 and new_order.price <= max(buy_orders).price:
            buy_orders.append(new_order)
            return
        orders_list1 = buy_orders
        orders_list2 = sell_orders

    else:
        if len(sell_orders) != 0 and new_order.price >= min(buy_orders).price:
            sell_orders.append(new_order)
            return
        orders_list1 = sell_orders
        orders_list2 = buy_orders


    executed = False

    for index, order in enumerate(orders_list2):
        if match_orders(new_order, order):
            dealSize = min(new_order.size, order.size)

            request = ContractRequest(new_order.user, order.user, order.price, dealSize)
            request.send()

            new_order.size -= dealSize
            order.size -= dealSize

            if new_order.size == 0:
                executed = True
                if order.size == 0:
                    orders_list2.pop(index)
                break
        else:
            break

    if not executed:
        orders_list1.append(new_order)


def print_tree(tree, name):
    print(name)
    for element in tree:
        print(element)


if __name__ == "__main__":
    order1 = Order(10, 1000, 1, False)
    order2 = Order(11, 1000, 3, True)
    time.sleep(2)
    order3 = Order(12, 900, 2, True)
    order4 = Order(14, 1000, 3, False)

    handle_new_order(order1)
    print_tree(buy_orders, "buy_orders")
    print_tree(sell_orders, "sell_orders")

    handle_new_order(order2)
    print_tree(buy_orders, "buy_orders")
    print_tree(sell_orders, "sell_orders")

    handle_new_order(order3)
    print_tree(buy_orders, "buy_orders")
    print_tree(sell_orders, "sell_orders")

    handle_new_order(order4)
    print_tree(buy_orders, "buy_orders")
    print_tree(sell_orders, "sell_orders")
