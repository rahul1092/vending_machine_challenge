from .Product import Product


class VendingMachine():
    """
    Simulates Vending Machine Operations
    """
    def __init__(self):
        """
        Initializes the Vending Machine
        """
        initialization_data = self.initialization_data()
        self.currency = initialization_data[0]
        self.product_dict = {}

        for product in initialization_data[1]:
            self.product_dict[product['id']] = [Product(
                product_id=product['id'], product_name=product['name'],
                price=product['price']), product['quantity']]

        self.coins = initialization_data[2]
        self.change_coins_allowed_qauntities = initialization_data[3]

    def initialization_data(self):
        """
        :return: Data used for initializing Vending Machine
        """
        currency = 'JYP'
        product_list = [
            {'id': 1, 'name': 'Canned coffee', 'price': 120, 'quantity': 5},
            {'id': 2, 'name': 'Water PET bottle', 'price': 100, 'quantity': 0},
            {'id': 3, 'name': 'Soft drinks', 'price': 150, 'quantity': 3}]
        coin_quantities = {10: 5, 50: 10, 100: 5, 500: 1}
        change_coins_minimum_allowed = {10: 9, 100: 4}

        return (currency, product_list, coin_quantities,
                change_coins_minimum_allowed)

    def are_input_coins_acceptable(self, coins_dict):
        """
        Checks if Input Coins be accepted as a valid amount based
        on change possible
        :return: True if coins acceptable Else False
        """
        def higher_value_coins_present(coins_dict, coin_value):
            for coin in coins_dict.items():
                if coin[0] > coin_value:
                    return True
            return False

        for change_coins in self.change_coins_allowed_qauntities.items():
            if self.coins[change_coins[0]] < change_coins[1] and \
                    higher_value_coins_present(coins_dict, change_coins[0]):
                return False

        return True

    def is_sale_possible(self, product_id, amount_inserted):
        """
        :return: True if sale possible, Else False
        """
        if self.product_dict[product_id][1] == 0:
            return False
        if self.product_dict[product_id][0].price > amount_inserted:
            return False

        return True

    def make_sale(self, product_id, amount_inserted):
        """
        Updates the Product count and returns change amount
        """
        product_info = self.product_dict[product_id]
        product_info[1] -= 1
        return amount_inserted - product_info[0].price

    def handle_input(self):
        """
        Handles user input and then takes relevant actions
        """
        pass

    def produce_display(self):
        """
        Creates a user interface for the vending machine
        """
        pass
