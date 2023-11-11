"""module used for item list operations"""
import math
import random

from shoppinglistapp.core.errors import (InvalidItemNameError, InvalidItemPriceError,
                         InvalidItemPoolError, NonExistingItemError,
                         DuplicateItemError)


class Item:
    """this class is used for editing existing item list from command"""
    def __init__(self, name, price):
        if not isinstance(name, str) or not name:
            raise InvalidItemNameError(name)
        self.name = name
        if isinstance(price, str) and '.' in price:
            split = price.split('.')
            if len(split) > 2:
                raise InvalidItemPriceError(price)
            if not split[0].isdigit():
                raise InvalidItemPriceError(price)
            if (not split[1].isdigit()) or (int(split[1]) < 0):
                raise InvalidItemPriceError(price)
            price = float(price)

        if not isinstance(price, (float, int)) or price <= 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        """get the order from the rounding up the log of price"""
        return math.floor(round(math.log(self.price, 10), 10))

    def get_price_str(self, quantity=None, hide_price=False, order=None):
        """get the price when different command is used"""
        if quantity is None:
            result_price = self.price
        else:
            result_price = quantity * self.price

        if order is None:
            order = 10 ** self.get_order()
        else:
            order = 10 ** order
        total_length = len(str(order)) + 3
        real_length = total_length - 3
        if order > result_price:
            print_price = f'${result_price:0>{total_length}.2f}'
        else:
            print_price = f'${result_price:.2f}'

        if hide_price:
            print_price = f'${"?" * (real_length)}.??'

        return print_price

    def get_list_item_str(self, quantity=None, leading_dash=True):
        """get the list of items when command is put"""
        if quantity is None:
            qnt_str = ''
        else:
            qnt_str = f' ({quantity}x)'

        dash = ''
        if leading_dash:
            dash = '- '
        return f'{dash}{self.name}{qnt_str}'
#    def item2line(self, quantity = None, hide_price = False, order = None,
#                  padding = 0,leading_dash = True):
        # quantity
#        if quantity is None:
#            qnt_str = ''
#        else:
#            qnt_str = f' ({quantity}x)'
#
#        # price
#        if order is None:
#            order = self.get_order()
#        prcStr = '${:0' + str(order + 4) + '.2f}'
#        prcStr = prcStr.format(self.price * (quantity or 1))
#        if hide_price:
#            prcStr = f'${"?" * (order + 1)}.??'
#
#        # dash
#        dash = ''
#        if leading_dash:
#            dash = '- '
#        return f'{dash}{self.name}{qnt_str} ...{"." * padding} {prcStr}'

    def __repr__(self):
        return f'Item({self.name}, {self.price})'

    def __eq__(self, other):
        return (isinstance(other, Item) and self.name == other.name and
                self.price == other.price)


class ItemPool:
    """class used to store item pool"""
    def __init__(self, items=None):
        if not items:
            items = {}
        if not isinstance(items, dict):
            raise InvalidItemPoolError()
        for key, val in items.items():
            if not isinstance(key, str) or not isinstance(val, Item):
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        """function to add item to the pool"""
        if not isinstance(item, Item):
            raise InvalidItemPoolError()
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        """function to remove item in the pool"""
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        """function to get the size of the pool"""
        return len(self.items)

    def sample_items(self, sample_size):
        """function to get a random number of item pool"""
        return (random.sample(list(self.items.values()),
                              min(sample_size, len(self.items))))

#    def show_items(self):
#        max_name, max_order = 0, 0
#        for item in self.items.values():
#            max_name = max(max_name, len(item.name))
#            max_order = max(max_order, item.get_order())
#        out = 'ITEMS\n'
#        for item_name in sorted(self.items.keys()):
#            item = self.items[item_name]
#            padding=max_name - len(item_name)
#            out += item.get_list_item_str() + "..." + "." * padding +
#                   item.get_price_str(order=max_order) + '\n'
#            out += item.item2line(padding=max_name - len(item_name),
#                   order=max_order) + '\n'
#        return out

    def __repr__(self):
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        return isinstance(other, ItemPool) and self.items == other.items
