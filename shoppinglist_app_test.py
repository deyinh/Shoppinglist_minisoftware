import math

import pytest

from shoppinglistapp.core.items import Item, ItemPool
from shoppinglistapp.core.errors import (InvalidItemNameError, InvalidItemPriceError,
                         InvalidItemPoolError, NonExistingItemError,
                         DuplicateItemError, InvalidShoppingListSizeError)
from shoppinglistapp.core.shoppinglist import ShoppingList
from shoppinglistapp.core.appengine import AppEngine


def test_valid_item_init():
    item = Item('bread', 3.25)
    assert item.name == 'bread'
    assert math.isclose(item.price, 3.25)


def test_invalid_item_init():
    with pytest.raises(InvalidItemNameError):
        Item('', 3.25)
    with pytest.raises(InvalidItemPriceError):
        Item('bread', -3.25)
    with pytest.raises(InvalidItemPriceError):
        Item('bread', '3.25.3')
    with pytest.raises(InvalidItemPriceError):
        Item('bread', 'f.2')
    with pytest.raises(InvalidItemPriceError):
        Item('bread', '2.f')
    with pytest.raises(InvalidItemPriceError):
        Item('bread', '2.-1')
    with pytest.raises(InvalidItemNameError):
        Item(3, 3.25)
    with pytest.raises(InvalidItemPoolError):
        ItemPool(items = list('bread'))
    with pytest.raises(InvalidItemPoolError):
        ItemPool(items = {3.25 : 'bread'})
    with pytest.raises(InvalidItemPoolError):
        item = ('bread', 3.25)
        ip = ItemPool(items = {'milk' : Item('milk', 2.15)})
        ip.add_item(item)
    with pytest.raises(NonExistingItemError):
        ip = ItemPool(items = {'milk' : Item('milk', 2.15)})
        ip.remove_item('bread')
    with pytest.raises(DuplicateItemError):
        item = Item('bread', 3.25)
        ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
        ip.add_item(item)
    with pytest.raises(InvalidShoppingListSizeError):
        ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
        ShoppingList(item_pool=ip, size=5)
    with pytest.raises(ValueError):
        ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
        sp = ShoppingList(item_pool=ip)
        sp.refresh(size=-1, quantities=[1], item_pool=ip) 
    with pytest.raises(ValueError):
        ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
        sp = ShoppingList(item_pool=ip)
        sp.refresh(size=1, quantities=1, item_pool=ip) 
    with pytest.raises(ValueError):
        ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
        sp = ShoppingList(item_pool=ip)
        sp.refresh(size=1, quantities=[-1], item_pool=ip) 


def test_item_get_order():
    item = Item('bread', 3.25)
    assert item.get_order() == 0
    item.price = 1000.0
    assert item.get_order() == 3


def test_item_get_list_item_str():
    item = Item('bread', 3.25)
    assert item.get_list_item_str() == '- bread'
    assert item.get_list_item_str(quantity=2) == '- bread (2x)'
    assert item.get_list_item_str(
        quantity=2, leading_dash=True) == '- bread (2x)'


def test_item_get_price_str():
    item = Item('bread', 3.25)
    assert item.get_price_str() == '$3.25'
    assert item.get_price_str(hide_price=True) == '$?.??'
    assert item.get_price_str(order=3) == '$0003.25'
    assert item.get_price_str(quantity=2) == '$6.50'


def test_item_repr():
    item = Item('bread', 3.25)
    assert repr(item) == 'Item(bread, 3.25)'

def test_item_eq():
    item1 = Item('bread', 3.25)
    item2 = Item('bread', 3.25)
    item3 = Item('butter', 4.10)
    assert item1 == item2
    assert item1 != item3

def test_itempool():
    ItemPool(items=None)

def test_add_item():
    item = Item('bread', 3.25)
    ip = ItemPool(items = {'milk' : Item('milk', 2.15)})
    ip.add_item(item)

def test_remove_item():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ip.remove_item('bread')

def test_item_price_str():
    Item('bread', '3.25')

def test_sample_items():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    assert ip.sample_items(1) == [Item('bread', 3.25)]

def test_itempool_repr_and_eq():
    ip1 = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ip2 = ItemPool(items = {'bread' : Item('bread', 3.25)})
    assert ip1 == ip2
    assert repr(ip1) == "ItemPool({'bread': Item(bread, 3.25)})"

def test_refresh_shopping_list_none():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    sp = ShoppingList(item_pool=ip)
    sp.refresh(item_pool=ip) 
    for i in range(1,10): 
        if sp.list == [(Item('bread', 3.25), i)]:
            assert sp.list == [(Item('bread', 3.25), i)]

def test_refresh_shopping_list_larger_size():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25), 'milk' : Item('milk', 2.15)})
    sp = ShoppingList(size=2, quantities=[1], item_pool=ip)
    sp.refresh(size=2, quantities=[1], item_pool=ip) 
    assert sp.list == [(Item('bread', 3.25), 1), (Item('milk', 2.15), 1)] or sp.list == [(Item('milk', 2.15), 1), (Item('bread', 3.25), 1)]

def test_refresh_shopping_list_smaller_size():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    sp = ShoppingList(size=1, quantities=[1,1], item_pool=ip)
    sp.refresh(size=1, quantities=[1,1], item_pool=ip) 
    assert sp.list == [(Item('bread', 3.25), 1)]

def test_other_shopping_list():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    sp = ShoppingList(size=1, quantities=[1,1],item_pool=ip)
    assert sp.get_total_price() == 3.25
    assert sp.get_item_price(0) == 3.25 
    assert len(sp) == 1

def test_app_engine_process_answer_1():
    ae = AppEngine()
    ae.process_answer('3.2.6') 
    assert ae.message == 'Your answer ("3.2.6") is not a number.'

def test_app_engine_process_answer_2():
    ae = AppEngine()
    ae.process_answer('m.2')
    assert ae.message == 'Your answer ("m.2") is not a number.'

def test_app_engine_process_answer_3():
    ae = AppEngine()
    ae.process_answer('mmm')
    assert ae.message == 'Your answer ("mmm") is not a number.'

def test_app_engine_process_answer_4():
    ae = AppEngine()
    ae.process_answer('2.m')
    assert ae.message == 'Your answer ("2.m") is not a number.'

def test_app_engine_process_answer_5():
    ae = AppEngine()
    ae.correct_answer = 3.24
    ae.process_answer('3.24')
    assert ae.message == 'Correct!'

def test_app_engine_process_answer_6():
    ae = AppEngine()
    ae.correct_answer = 3.24
    ae.process_answer(3.20)
    assert ae.message == ('Not Correct! (Expected $3.24)\nYou answered $3.20.')

def test_process_add_item_1():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: 0.99')
    assert ae.message == 'Banana (0.99) added successfully.'

def test_process_add_item_2():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: 3.2.6')
    assert ae.message == ("could not convert string to float: '3.2.6'")

def test_process_add_item_3():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: m.2')
    assert ae.message == ("could not convert string to float: 'm.2'")

def test_process_add_item_4():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: 2.m')
    assert ae.message == ("could not convert string to float: '2.m'")

def test_process_add_item_5():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: 2.-1')
    assert ae.message == ("could not convert string to float: '2.-1'")

def test_process_add_item_6():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: price')
    assert ae.message == ("could not convert string to float: 'price'")

def test_process_add_item_7():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: -1')
    assert ae.message == ('The price argument ("-1.0") does not appear to be any of the following: float, an integer, or a string that can be parsed to a non-negative float.')
    
def test_process_add_item_8():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add Banana: 1')
    assert ae.message == 'Banana (1.0) added successfully.'

def test_process_add_item_9():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add : 0.99')
    assert ae.message == 'Item name string cannot be empty.'

def test_process_add_item_10():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add bread: 3.25')
    assert ae.message == 'Duplicate!'

def test_process_add_item_11():
    ip = ItemPool(items = {'bread' : Item('bread', 3.25)})
    ae = AppEngine(items=ip)
    ae.process_add_item('add bread 3.25')
    assert ae.message == 'Cannot add "bread 3.25".\nUsage: add <item_name>: <item_price>'

def test_process_del_item_1():
    ip = ItemPool(items = {'Bread' : Item('Bread', 3.25), 'Milk' : Item('Milk', 2.15)})
    ae = AppEngine(items=ip)
    ae.process_del_item('del Milk')
    assert ae.message == 'Milk removed successfully.'

def test_process_del_item_2():
    ip = ItemPool(items = {'Bread' : Item('Bread', 3.25), 'Milk' : Item('Milk', 2.15)})
    ae = AppEngine(items=ip)
    ae.process_del_item('del Jam')
    assert ae.message == 'Item named "Jam" is not present in the item pool.'