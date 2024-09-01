import unittest
import store_inputs as s
from unittest.mock import mock_open, patch
from roaming_simulator import RoamingSimulator


class TestRoamingSimulator(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data= s.initial_connection)
    def test_initial_connection(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'].name)
        self.assertEqual(len(x.ap_dict['AP1'].clients), 1)
        self.assertIs(x.ap_dict['AP1'].clients[0], x.client_dict['Client1'])

    @patch('builtins.open', new_callable=mock_open, read_data= s.initial_connection2)
    def test_initial_connection2(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client2'].connected, x.ap_dict['AP2'].name)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'].name)
        self.assertIn(x.client_dict['Client1'],x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client2'],x.ap_dict['AP2'].clients)

    @patch('builtins.open', new_callable=mock_open, read_data= s.client_limit)
    def test_AP_client_limit(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'].name)
        self.assertEqual(x.client_dict['Client2'].connected, x.ap_dict['AP1'].name)
        self.assertEqual(x.client_dict['Client3'].connected, x.ap_dict['AP1'].name)
        self.assertEqual(x.client_dict['Client4'].connected, x.ap_dict['AP1'].name)
        self.assertIn(x.client_dict['Client1'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client2'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client3'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client4'], x.ap_dict['AP1'].clients)
        self.assertEqual(x.client_dict['Client5'].connected, None)
        self.assertNotIn(x.client_dict['Client5'], x.ap_dict['AP1'].clients)

    @patch('builtins.open', new_callable=mock_open, read_data= s.access_controller)
    def test_access_controller(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.ap_dict['AP1'].channel, 11)
        self.assertEqual(x.ap_dict['AP2'].channel, 1)
        self.assertEqual(x.ap_dict['AP3'].channel, 2)
        self.assertEqual(x.ap_dict['AP4'].channel, 6)

    @patch('builtins.open', new_callable=mock_open, read_data= s.ac_no_overlap)
    def test_no_overlap(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.ap_dict['AP1'].channel, 6)
        self.assertEqual(x.ap_dict['AP2'].channel, 6)
        self.assertEqual(x.ap_dict['AP3'].channel, 6)

    @patch('builtins.open', new_callable=mock_open, read_data = s.move_inside)
    def test_move_within_coverage(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'].name)
        self.assertEqual(x.client_dict['Client1'].coord, (10,10))

    @patch('builtins.open', new_callable=mock_open, read_data = s.move_outside)
    def test_move_outside_coverage(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].coord, (20,20))
        self.assertEqual(x.client_dict['Client1'].connected, None)
        print(x.client_dict['Client1'].log)
        print(x.ap_dict['AP1'].log)








if __name__ == '__main__':
    unittest.main()

