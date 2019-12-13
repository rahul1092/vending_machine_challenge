import os
from subprocess import call
from VendingMachine import VendingMachine
import ipdb

class TerminalAdapter():
    """
    Acts as a terminal interface for the VendingMachine
    """
    def __init__(self):
        self.vending_machine = VendingMachine()
        self.product_to_be_sold = None
        self.error_msg = None

    def __call__(self, *args, **kwargs):
        while True:
            # ipdb.set_trace()
            self.produce_display()
            # ipdb.set_trace()
            self.handle_input()

    def handle_input(self, input_value=None):
        """
        Handles user input and then takes relevant actions
        """
        if not input_value:
            input_value = input().strip()
        if not input_value:
            self.handle_input()

        input_value_list = list(map(int, input_value.split()))
        input_command = input_value_list[0]
        input_args = []
        if len(input_value_list) > 1:
            input_args = input_value_list[1:]

        if input_command == 1 and input_args and \
                self.vending_machine.command_allowed(input_command):
            coins_acceptable = self.vending_machine.set_amount_inserted(input_args)
            if not coins_acceptable:
                self.error_msg = 'Invalid amount inserted. Please try again'

        if input_command == 2 and input_args and \
                self.vending_machine.command_allowed(input_command):
            # import ipdb; ipdb.set_trace()
            sale_success = self.vending_machine.make_sale(input_args[0])
            if not sale_success:
                self.error_msg = 'Unable to make sale. Please try again'
            # return self.produce_display(input_command, sale_success)

        if input_command == 3 and self.vending_machine.command_allowed(input_command):
            success = self.vending_machine.set_item_at_outlet()
            # return self.handle_input(3, success)

        if input_command == 4 and self.vending_machine.command_allowed(input_command):
            return_val = self.vending_machine.get_change_amount()
            # return self.handle_input(4, return_val)

        if input_command == 5 and self.vending_machine.command_allowed(input_command):
            return_val = self.vending_machine.get_coins_from_return_gate()
            # return self.handle_input(5, return_val)

    def produce_display(self):
        """
        Produces terminal output on the basis of Vending Machine state
        """
        call('clear' if os.name == 'posix' else 'cls')
        curreny = self.vending_machine.get_currency()
        input_amount = self.vending_machine.get_input_amount()
        change_coins_state = self.vending_machine.get_current_change_status()
        print('---------------------------------------------')
        print(f'[Input amount]\t\t{input_amount} {curreny}')
        change_coin_text = '[Change]\t'
        not_first = False
        for change_coins in change_coins_state.items():
            if not_first:
                change_coin_text += '\t'
            not_first = True
            change_coin_text += f'\t{str(change_coins[0])} {curreny} \t {change_coins[1]}\n'
        print(change_coin_text)
        return_gate_text = '[Return gate]\t'
        # import ipdb; ipdb.set_trace()
        return_coins = self.vending_machine.get_change_coins_dict()

        if return_coins:
            return_coins_list = list(return_coins.keys())
            return_coins_list.sort()
            for return_coin in return_coins_list:
                for _ in range(0, return_coins[return_coin]):
                    return_gate_text += f'\t\t{return_coin} {curreny}\n'
        else:
            return_gate_text += 'Empty\n'
        print(return_gate_text)

        items_for_sale_text = '[Items for sale]'
        product_details_list = self.vending_machine.get_product_details_list()
        not_first = False
        for product in product_details_list:
            if not_first:
                items_for_sale_text += '\t\t'
            not_first = True
            items_for_sale_text += f'\t {product["id"]}. {product["name"]} \t ' \
                                   f'{product["price"]} {curreny}\n'
        print(items_for_sale_text)
        outlet_text = f'[Outlet]'
        items_in_outlet = self.vending_machine.get_items_in_outlet_list()
        not_first = False
        for product_id in items_in_outlet:
            if not_first:
                outlet_text += '\t'
            not_first = True
            outlet_text += f'\t {self.vending_machine.get_product_details(product_id)["name"]} \n'
        print(outlet_text)
        if self.error_msg:
            print(f'Error : {self.error_msg}')
        self.error_msg = None
        print('---------------------------------------------')
