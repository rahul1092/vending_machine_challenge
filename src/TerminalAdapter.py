import os
from subprocess import call
from constants import *
from VendingMachine import VendingMachine


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
            self.produce_display()
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

        valid_command, valid_states = self.vending_machine.command_allowed(
            input_command)
        if not valid_command:
            self.error_msg = f'Wrong command selected. Allowed command ' \
                             f'at this stage {str(valid_states)}'
            return

        if input_command == INPUT_ACCEPTANCE and input_args:
            coins_acceptable = self.vending_machine.set_amount_inserted(
                input_args)
            if not coins_acceptable:
                self.error_msg = 'Invalid amount inserted. Please try again'

        if input_command == PRODUCT_BUYING_INFO and input_args:
            # import ipdb; ipdb.set_trace()
            sale_success = self.vending_machine.make_sale(input_args[0])
            if not sale_success:
                self.error_msg = 'Unable to make sale. Please try again'

        if input_command == ITEM_AT_OUTLET:
            self.vending_machine.set_item_at_outlet()

        if input_command == CHANGE_AMOUNT_PRODUCTION:
            self.vending_machine.get_change_amount()

        if input_command == CHANGE_AT_RETURN_GATE:
            self.vending_machine.get_coins_from_return_gate()

        if input_command == MACHINE_SHUT_DOWN:
            self.vending_machine.shut_down()

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
                                   f'{product["price"]} {curreny} \t {product["status"]} \n'
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
