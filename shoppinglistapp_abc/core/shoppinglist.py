"""this module is used to store operation for shoppinglist"""
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
import random
from shoppinglistapp.core.errors import *
from shoppinglistapp.core.items import *


class ShoppingList:
    """this class is used for shopping list operation"""
    def __init__(self, size=None, quantities=None, item_pool=None):
        self.list = []
        if item_pool is not None:
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size=None, quantities=None):
        """this function is used to refresh shopping list"""
        if size is None:
            size = random.randint(1, item_pool.get_size())
        if not isinstance(size, int) or size < 1:
            raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if not isinstance(quantities, list):
            raise ValueError()
        for elem in quantities:
            if not isinstance(elem, int) or elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        items_list = item_pool.sample_items(size)
        self.list = list(zip(items_list, quantities))
#        self.list = [(item, q) for item, q in zip(items_list, quantities)]

    def get_total_price(self):
        """this function is used for total price calculation"""
        return round(sum(list(item.price * qnt for item, qnt in self.list)), 2)

    def get_item_price(self, i):
        """this function is used to get price for individual item"""
        return round(self.list[i][0].price * self.list[i][1], 2)

    def __len__(self):
        return len(self.list)
