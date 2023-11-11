"""module used to detect different kinds of input errors"""


class InvalidItemNameError(Exception):
    """this class is used when there is item name input errors"""
    def __init__(self, item):
        if not isinstance(item, str):
            super().__init__(f'Item name must be a string (not {type(item)}).')
        else:
            super().__init__('Item name string cannot be empty.')


class InvalidItemPriceError(Exception):
    """this class is used when name is correct but price input has errors"""
    def __init__(self, price):
        super().__init__(f'The price argument ("{price}") \
                         does not appear to be any of the following: float, \
                         an integer, or a string that can be parsed to a \
                         non-negative float.')


class InvalidItemPoolError(Exception):
    """this class is used when items pool has keys
    and values with error setted"""
    def __init__(self):
        super().__init__('ItemsPool needs to be \
                         set as a dictionary with non-empty strings \
                         as keys and Item instances as values.')


class NonExistingItemError(Exception):
    """this class is used when the input item name
    does not exist in the item pool"""
    def __init__(self, item_name):
        super().__init__(f'Item named "{item_name}" \
                         is not present in the item pool.')


class DuplicateItemError(Exception):
    """class is used when the input item that needed
    to be added has already in the item pool"""
    def __init__(self):
        super().__init__('Duplicate!')


class InvalidShoppingListSizeError(Exception):
    """this class is used when the list size input is invalid"""
    def __init__(self):
        super().__init__('Invalid List Size!')
