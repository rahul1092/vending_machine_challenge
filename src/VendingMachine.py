import sys
from collections import Counter
from constants import *
from Product import Product


class VendingMachine():
    """
    Simulates Vending Machine Operations
    """
    def __init__(self):
        """
        Initializes the Vending Machine
        """
        initialization_data = self.__initialization_data()
        self.currency = initialization_data[0]
        self.product_dict = {}
        self.sale_item_ids = []

        for product in initialization_data[1]:
            self.product_dict[product['id']] = [Product(
                product_id=product['id'], product_name=product['name'],
                price=product['price']), product['quantity']]

        self.coins = initialization_data[2]
        self.change_coins_allowed_quantities = initialization_data[3]
        self.current_state = INITIAL_STAGE
        self.amount_inserted = 0
        self.change_coins_dict = {}
        self.amount_left = None

    def __initialization_data(self):
        """
        :return: Data used for initializing Vending Machine
        """
        currency = 'JYP'
        product_list = [
            {'id': 1, 'name': 'Canned coffee', 'price': 120, 'quantity': 5},
            {'id': 2, 'name': 'Water PET bottle', 'price': 100, 'quantity': 0},
            {'id': 3, 'name': 'Soft drinks', 'price': 150, 'quantity': 3}]
        coin_quantities = {10: 10, 50: 10, 100: 5, 500: 1}
        change_coins_minimum_allowed = {10: 9, 100: 4}

        return (currency, product_list, coin_quantities,
                change_coins_minimum_allowed)

    def __are_input_coins_acceptable(self, coins_list):
        """
        Checks if Input Coins be accepted as a valid amount based
        on change possible
        :return: True if coins acceptable Else False
        """
        coins_dict = Counter(coins_list)

        def higher_value_coins_present(coins_dict, coin_value):
            for coin in coins_dict.items():
                if coin[0] > coin_value:
                    return True
            return False

        coin_value = sum(coins_list)
        purchase_possible = False
        for product in self.product_dict.items():
            if product[1][0].price <= coin_value:
                purchase_possible = True
                break
        if not purchase_possible:
            return False

        for change_coins in self.change_coins_allowed_quantities.items():
            if self.coins[change_coins[0]] < change_coins[1] and \
                    higher_value_coins_present(coins_dict, change_coins[0]):
                return False

        return True

    def __is_sale_possible(self, product_id):
        """
        Returns True if sale possible, Else False
        """
        if product_id not in self.product_dict:
            return False
        if self.product_dict[product_id][1] == 0:
            return False
        if self.product_dict[product_id][0].price > self.amount_left:
            return False

        return True

    def __get_change_coins(self, change_amount):
        """
        Returns a dictionary of the coins that corresspond to the change
        that can be returned to the user
        """
        amount_left = change_amount
        change_coin_dict = {}
        if not self.amount_inserted_list:
            return {}
        change_dict = Counter(self.amount_inserted_list)
        coins_copy = self.coins.copy()
        for coins in change_dict.items():
            coins_copy[coins[0]] += coins[1]

        coins_list = list(self.coins.keys())
        coins_list.sort(reverse=True)

        for coin in coins_list:
            usable = amount_left // coin
            if usable >= 1 and amount_left > 0:
                if coins_copy[coin] >= usable:
                    amount_left -= (usable * coin)
                    change_coin_dict[coin] = usable
                    coins_copy[coin] -= usable
                elif coins_copy[coin]:
                    amount_left -= (coins_copy[coin] * coin)
                    change_coin_dict[coin] = coins_copy[coin]
                    coins_copy[coin] = 0

        if amount_left > 0:
            return {}
        return change_coin_dict

    def __add_inserted_coins_to_pool(self):
        """
        Adds the coins entered for purchase to coin pool
        """
        for coin in self.amount_inserted_list:
            self.coins[coin] += 1

    def __get_product_status_text(self, product_id):
        """
        Returns product status displayed on terminal
        """
        if self.product_dict[product_id][1] == 0:
            return 'Sold out'
        if self.amount_left and self.product_dict[product_id][0].price <= self.amount_left:
            return 'Can Purchase'
        return ''

    def get_currency(self):
        """
        Returns money currency
        """
        return self.currency

    def set_amount_inserted(self, amount_inserted_list):
        """
        Sets the coins that were inserted in the vending machine
        """
        self.amount_inserted = sum(amount_inserted_list)
        self.amount_inserted_list = amount_inserted_list
        self.amount_left = self.amount_inserted
        coins_acceptable = self.__are_input_coins_acceptable(
            self.amount_inserted_list)
        if coins_acceptable:
            self.current_state = INPUT_ACCEPTANCE
        return coins_acceptable

    def make_sale(self, product_id):
        """
        Updates the Product count and returns change amount
        """
        sale_possible = self.__is_sale_possible(product_id)
        if not sale_possible:
            self.sale_success = False
            return False

        product_info = self.product_dict[product_id]
        product_info[1] -= 1
        self.return_amount = self.amount_left - product_info[0].price
        self.amount_left -= product_info[0].price
        self.sale_success = True
        self.sale_item_ids.append(product_id)
        self.current_state = PRODUCT_BUYING_INFO
        return True

    def get_items_in_outlet_list(self):
        """
        Returns list if ids for products which can be put in outlet
        """
        return self.sale_item_ids.copy()

    def set_item_at_outlet(self):
        """
        Moves purchased items to outlet
        """
        if self.sale_success:
            self.item_at_oulet = True
            self.sale_item_ids = []
            self.current_state = ITEM_AT_OUTLET
            return True
        return False

    def get_change_amount(self):
        """
        Returns the details of the change
        """
        if not self.sale_success:
            return False, {}

        change_coins_dict = {}
        if self.return_amount:
            change_coins_dict = self.__get_change_coins(self.return_amount)
            if not change_coins_dict:
                return False, {}

        if change_coins_dict:
            for coin in change_coins_dict.items():
                self.coins[coin[0]] -= coin[1]

        self.__add_inserted_coins_to_pool()
        self.amount_inserted = 0
        self.change_coins_returned = True
        self.change_coins_dict = change_coins_dict
        self.current_state = CHANGE_AMOUNT_PRODUCTION
        return True, change_coins_dict

    def get_coins_from_return_gate(self):
        """
        Removes coins from return gate
        """
        if self.change_coins_returned:
            self.reset_to_initial()
            self.current_state = CHANGE_AT_RETURN_GATE
            return True
        return False

    def get_current_change_status(self):
        """
        Returns details of availability of change
        """
        change_coins_state = {}
        for coin in self.change_coins_allowed_quantities.items():
            change_coins_state[coin[0]] = "Change" \
                if self.coins[coin[0]] >= coin[1] else "No Change"
        return change_coins_state

    def get_product_details_list(self):
        """
        Returns the list of products that are displayed on the terminal
        """
        product_ids = list(self.product_dict.keys())
        product_ids.sort()
        product_listing = [self.get_product_details(
            product_id) for product_id in product_ids]
        return product_listing

    def get_product_details(self, product_id):
        """
        Returns a dictionary containing information about a product
        """
        product_info = {}
        product_info['id'] = product_id
        product_info['name'] = self.product_dict[product_id][0].product_name
        product_info['price'] = self.product_dict[product_id][0].price
        product_info['status'] = self.__get_product_status_text(product_id)
        return product_info

    def shut_down(self):
        """
        Exits the program
        """
        sys.exit()

    def get_input_amount(self):
        """
        Returns the value of amount inserted by the user
        """
        return self.amount_inserted

    def get_change_coins_dict(self):
        """
        Returns the dictionary containing information of change
        """
        return self.change_coins_dict

    def reset_to_initial(self):
        """
        Resets the vending machine to Input acceptance state
        """
        self.amount_inserted = 0
        self.amount_inserted_list = []
        self.return_amount = 0
        self.sale_success = None
        self.item_at_oulet = None
        self.change_coins_dict = {}
        self.amount_left = None
        self.current_state = INITIAL_STAGE

    def command_allowed(self, input_command):
        """
        Checks if the input command is allowed for the given state
        of the vending machine
        """
        if self.current_state == INITIAL_STAGE and input_command not in \
                [INPUT_ACCEPTANCE]:
            return False, [INPUT_ACCEPTANCE]

        if self.current_state == INPUT_ACCEPTANCE and input_command \
                not in [INPUT_ACCEPTANCE, PRODUCT_BUYING_INFO]:
            return False, [INPUT_ACCEPTANCE, PRODUCT_BUYING_INFO]

        if self.current_state == PRODUCT_BUYING_INFO and input_command \
                not in [PRODUCT_BUYING_INFO, ITEM_AT_OUTLET]:
            return False, [PRODUCT_BUYING_INFO, ITEM_AT_OUTLET]

        if self.current_state == ITEM_AT_OUTLET and input_command \
                not in [CHANGE_AMOUNT_PRODUCTION]:
            return False, [CHANGE_AMOUNT_PRODUCTION]

        if self.current_state == CHANGE_AMOUNT_PRODUCTION and \
                input_command not in [CHANGE_AT_RETURN_GATE]:
            return False, [CHANGE_AT_RETURN_GATE]

        if self.current_state == CHANGE_AT_RETURN_GATE and \
                input_command not in [INPUT_ACCEPTANCE, MACHINE_SHUT_DOWN]:
            return False, [INPUT_ACCEPTANCE, MACHINE_SHUT_DOWN]

        return True, []
