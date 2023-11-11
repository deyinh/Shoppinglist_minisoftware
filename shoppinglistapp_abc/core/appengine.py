"""this module is the engine of app_cli.py"""
import sys
sys.path.insert(0, 'core')
# pylint: disable=wrong-import-position
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from shoppinglistapp.core.items import *  # noqa: E402
from shoppinglistapp.core.shoppinglist import *  # noqa: E402


class AppEngine:
    """this class is used for main operative calculation of app"""
    def __init__(self, shopping_list=None, items=None):
        self.items = items
        self.shopping_list = shopping_list
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

    def process_answer(self, cmd):
        """this function is used to determine if input is integer or float"""
        if (isinstance(cmd, str) and '.' in cmd):
            split = cmd.split('.')
            if len(split) > 2:
                answer = None
            elif not split[0].isdigit():
                answer = None
            elif (not split[1].isdigit()) or (int(split[1]) < 0):
                answer = None
            else:
                answer = round(float(cmd), 2)
        elif (isinstance(cmd, str) and not cmd.isdigit()):
            answer = None
        else:
            answer = round(float(cmd), 2)
        if answer is not None:
            if answer == self.correct_answer:
                self.message = 'Correct!'
            else:
                self.message = ('Not Correct! (Expected '
                                f'${self.correct_answer:.02f})\n'
                                'You answered '
                                f'${answer:.02f}.')
        else:
            self.message = 'Your answer ("' + cmd + '") is not a number.'
#            self.message = 'The provided answer is not a valid number!'
        self.correct_answer = None

    def process_add_item(self, cmd):
        """this function is used to process when command needs to add items"""
        # pylint: disable=too-many-branches
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple) == 2:
            if (isinstance(item_tuple[1], str) and '.' in item_tuple[1]):
                split = item_tuple[1].split('.')
                if len(split) > 2:
                    answer = None
                elif not split[0].isdigit():
                    answer = None
                elif (not split[1].isdigit()) or (int(split[1]) < 0):
                    answer = None
                else:
                    answer = round(float(item_tuple[1]), 2)
            elif (isinstance(item_tuple[1], str) and not item_tuple[1].isdigit()):
                try:
                    answer = round(float(item_tuple[1]), 2)
                except ValueError:
                    answer = None
            else:
                answer = round(float(item_tuple[1]), 2)
        else:
            answer = item_tuple

        if answer is not None:
            if len(item_tuple) == 2:
                name, price = item_tuple
                if not name:
                    self.message = "Item name string cannot be empty."
                elif name in self.items.items:
                    self.message = "Duplicate!"
                elif float(price) < 0:
                    price = str(round(float(price), 1))
                    self.message = (f'The price argument ("{price}") does not appear to be any of the following: float, an integer, or a string that can be parsed to a non-negative float.')
                else:
                    item = Item(name, price)
                    self.items.add_item(item)
                    self.message = f'{name} ({float(price)}) added successfully.'
#                    self.message = f'{item} added successfully.'
            else:
                self.message = f'Cannot add "{item_str}".\n'
                self.message += 'Usage: add <item_name>: <item_price>'
        else:
            self.message = ("could not convert string to float: '" +
                            item_tuple[1] + "'")

    def process_del_item(self, cmd):
        """this function is used when command wants to delete item from pool"""
        item_name = cmd[4:]
        if item_name in self.items.items:
            self.items.remove_item(item_name)
            self.message = f'{item_name} removed successfully.'
        else:
            self.message = f'Item named "{item_name}" is not present in the item pool.'
