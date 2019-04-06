#include <iostream>
#include <list>
#include <algorithm>
#include <set>

const bool BUY = false;
const bool SELL = true;

class Order {
	int _user;
	int _time;
	int _price;
	int _size;
	bool _direction; //true - sell, false - buy
	int _status;

public:
	Order(__MESSAGE__): _user(__MESSAGE__.user) time(__TIMESTAMP__), _price(__MESSAGE__.price), 
		_size(__MESSAGE__.size), _direction(__MESSAGE__.direction), _status(1) {} 

	Order(int user, int price, int size, bool direction): _user(user), 
		time(__TIMESTAMP__), _price(price), _size(size), _direction(direction), _status(1) {} 

	int getTime() const {
		return _time;
	}

	int getPrice() const {
		return _price;
	}

	int getSize() const {
		return _size;
	}

	bool getDirection() const {
		return _direction;
	}

	int getUser() const {
		return _user;
	}

	void changeSize(int dealSize) {
		_size -= dealSize;
	}

	bool operator<(Order& order) const {
		if (_price < order._price) {
			return true;
		}
		else if (_price > order._price) {
			return false;
		}
		else if (_time < order._time) {
			return true;
		}
		else {
			return false;
		}
	}
}

class ContractRequest {
	int _buyerInformation;
	int _sellerInformation;
	int _price;
	int _size;


public:
	ContractRequest(buyInfo, sellInfo, price, size): _buyerInformation(buyInfo), _sellerInformation(sellInfo), _price(price), _size(size) {}


	//Это ещё предстоит сделать, здесь просто фигня для дебага всякого
	int send() {
		std::cout << "Buyer: " << _buyerInformation << std::endl;
		std::cout << "Seller: " << _buyerInformation << std::endl;
		std::cout << "Price: " << _buyerInformation << std::endl;
		std::cout << "Size: " << _buyerInformation << std::endl;

	}
};

bool matchOrders(Order& buyer, Order& seller) {
	if (buyer.getDirection == SELL) {
		throw "BUYER IS SELLER"
	}

	if (seller.getPrice() < buyer.getPrice()) {
		return false;
	}
	else {
		return true;
	}
}



void sendAndChangeOrders(Order& buyer, Order& seller) {

}


int main() {
	std::set<Order> buyOrders, sellOrders;


	while (true) {
		if (!__MESSAGE__) {
			continue;
		}

		Order newOrder(__MESSAGE__);
		if (newOrder.getDirection() == BUY) {
			//matching with sellers list

			//нужно проверить, является ли её стоимость наибольшей среди заявок на покупку
			//если это не так, то ей уже точно не подойдёт ни одна заявка на продажу
			if (newOrder.getPrice() <= buyOrders.rbegin()->getPrice()) {
				buyOrders.push(newOrder);
				continue;
			}

			bool executed = false;

			for (auto it = sellOrders.begin(); it != sellOrders.end(); sellOrders.erase(it++)) {
				order = *it;
				if (matchOrders(newOrder, order)) {
					//здесь надо кидать запрос смарт контракту, изменять заявки и удалять их, если они были исполнены

					int dealSize = std::max(newOrder.getSize(), order.getSize());

					ContractRequest request(newOrder.getUser(), order.getUser(), 
						order.getPrice(), dealSize);

					request.send();

					newOrder.changeSize(dealSize);
					order.changeSize(dealSize);

					if (newOrder.getSize() == 0) {
						executed = true;
						if (order.getSize() == 0) {
							sellOrders.erase(it);
						}
						break;
					}
				}
				else {
					break;
				}
			}

			//теперь после обработки заявки мы кидаем её в стакан, если она ещё не исполнена
			if (!executed) {
				buyOrders.push(newOrder);
			}

			//вроде всё, заявка обработана
		}
		else {
			//matching with buyers list
			//здесь всё так же как и при работе со списком заявок на продажу
			//только кое-где меняются местами order и newOrder

			if (newOrder.getPrice() >= sellOrders.begin()->getPrice()) {
				sellOrders.push(newOrder);
				continue;
			}

			bool executed = false;

			for (auto it = buyOrders.begin(); it != buyOrders.end(); buyOrders.erase(it++)) {
				order = *it;
				if (matchOrders(order, newOrder)) {

					int dealSize = std::max(order.getSize(), newOrder.getSize());

					ContractRequest request(order.getUser(), newOrder.getUser(), 
						newOrder.getPrice(), dealSize);

					request.send();

					newOrder.changeSize(dealSize);
					order.changeSize(dealSize);

					if (newOrder.getSize() == 0) {
						executed = true;
						if (order.getSize() == 0) {
							sellOrders.erase(it);
						}
						break;
					}
				}
				else {
					break;
				}
			}

			if (!executed) {
				buyOrders.push(newOrder);
			}
		}

	}
	return 0;
}