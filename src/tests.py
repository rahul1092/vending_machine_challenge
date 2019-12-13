import unittest
import mock
from constants import *
from VendingMachine import VendingMachine


class TestVendingMachine(unittest.TestCase):
    """
    Tests for VendingMachine
    """
    def setUp(self):
        """Test setup"""
        self.vending_machine = VendingMachine()

    @mock.patch('VendingMachine.VendingMachine.are_input_coins_acceptable',
                mock.MagicMock(return_value=True))
    def test_set_amount_inserted_sets_amount_correctly(self):
        """
        Tests that set_amount_inserted() sets the inserted amount
        correctly
        """
        return_value = self.vending_machine.set_amount_inserted(
            [10, 50, 10, 100])
        self.assertEqual(self.vending_machine.amount_inserted_list,
                         [10, 50, 10, 100])
        self.assertEqual(self.vending_machine.current_state,
                         INPUT_ACCEPTANCE)
        self.assertTrue(return_value)

    @mock.patch('VendingMachine.VendingMachine.is_sale_possible',
                mock.MagicMock(return_value=False))
    def test_check_make_sale_returns_false_if_sale_not_possible(self):
        """
        Tests that make_sale returns False if sale is not possible
        """
        self.assertFalse(self.vending_machine.make_sale(1))

    @mock.patch('VendingMachine.VendingMachine.is_sale_possible',
                mock.MagicMock(return_value=True))
    def test_make_sale_post_conditions(self):
        """
        Tests that make_sale sets the object variables correctly
        """
        vending_machine = VendingMachine()
        vending_machine.amount_left = 100
        product_info = vending_machine.product_dict[1]
        product_price = product_info[0].price
        vending_machine.make_sale(1)
        self.assertEqual(vending_machine.amount_left, 100 - product_price)
        self.assertTrue(vending_machine.sale_success)
        self.assertEqual(vending_machine.current_state, PRODUCT_BUYING_INFO)
        self.assertTrue(1 in vending_machine.sale_item_ids)


if __name__ == '__main__':
    unittest.main()
