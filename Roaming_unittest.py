import unittest
import store_inputs as s
from unittest.mock import mock_open, patch
from roaming_simulator import RoamingSimulator


class TestRoamingSimulator(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=s.initial_connection)
    def test_initial_connection1(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'])
        self.assertEqual(len(x.ap_dict['AP1'].clients), 1)
        self.assertIs(x.ap_dict['AP1'].clients[0], x.client_dict['Client1'])

    @patch('builtins.open', new_callable=mock_open, read_data=s.initial_connection2)
    def test_initial_connection2(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client2'].connected, x.ap_dict['AP2'])
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'])
        self.assertIn(x.client_dict['Client1'],x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client2'],x.ap_dict['AP2'].clients)

    @patch('builtins.open', new_callable=mock_open, read_data=s.client_limit)
    def test_AP_client_limit(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'])
        self.assertEqual(x.client_dict['Client2'].connected, x.ap_dict['AP1'])
        self.assertEqual(x.client_dict['Client3'].connected, x.ap_dict['AP1'])
        self.assertEqual(x.client_dict['Client4'].connected, x.ap_dict['AP1'])
        self.assertIn(x.client_dict['Client1'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client2'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client3'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client4'], x.ap_dict['AP1'].clients)
        self.assertEqual(x.client_dict['Client5'].connected, None)
        self.assertNotIn(x.client_dict['Client5'], x.ap_dict['AP1'].clients)

    @patch('builtins.open', new_callable=mock_open, read_data=s.access_controller)
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
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP1'])
        self.assertEqual(x.client_dict['Client1'].coord, (10,10))

    @patch('builtins.open', new_callable=mock_open, read_data=s.move_outside)
    def test_move_outside_coverage(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].coord, (20,20))
        self.assertEqual(x.client_dict['Client1'].connected, None)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming1)
    def test_roaming_to_ap(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP2'])
        self.assertEqual(x.client_dict['Client1'].coord, (25, 25))
        self.assertNotIn(x.client_dict['Client1'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client1'], x.ap_dict['AP2'].clients)
        self.assertIn('Step 1: Client1 ROAM TO AP2', x.ap_dict['AP2'].log)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming2)
    def test_fast_roaming(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP2'])
        self.assertEqual(x.client_dict['Client1'].coord, (25, 25))
        self.assertNotIn(x.client_dict['Client1'], x.ap_dict['AP1'].clients)
        self.assertIn(x.client_dict['Client1'], x.ap_dict['AP2'].clients)
        self.assertIn('Step 1: Client1 FAST ROAM TO AP2', x.ap_dict['AP2'].log)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming3)
    def test_denied_roaming(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, None)
        self.assertEqual(x.client_dict['Client1'].coord, (25, 25))
        self.assertNotIn(x.client_dict['Client1'], x.ap_dict['AP2'].clients)
        self.assertIn('Step 2: Client1 TRIED AP2 BUT WAS DENIED', x.ap_dict['AP2'].log)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming4)
    def test_multiple_movement(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].coord, (63, 63))
        self.assertEqual(x.ap_dict['AP1'].log,['Step 1: Client1 CONNECT LOCATION 5 5 WiFi4 2.4/5 true true true', 'Step 2: Client1 DISCONNECTS AT LOCATION 5 5'])
        self.assertEqual(x.ap_dict['AP2'].log,['Step 1: Client1 FAST ROAM TO AP2', 'Step 2: Client1 CONNECT LOCATION 21 21 WiFi4 2.4/5 true true true', 'Step 3: Client1 DISCONNECTS AT LOCATION 21 21'])
        self.assertEqual(x.ap_dict['AP3'].log,['Step 1: Client1 FAST ROAM TO AP3', 'Step 2: Client1 CONNECT LOCATION 42 42 WiFi4 2.4/5 true true true', 'Step 3: Client1 DISCONNECTS AT LOCATION 42 42'])
        self.assertEqual(x.ap_dict['AP4'].log,['Step 1: Client1 FAST ROAM TO AP4', 'Step 2: Client1 CONNECT LOCATION 63 63 WiFi4 2.4/5 true true true'])

    @patch('builtins.open', new_callable=mock_open, read_data=s.ap_evaluation)
    def test_AP_evaluation(self, mock_file):
        x = RoamingSimulator(mock_file)
        self.assertEqual(x.client_dict['Client1'].connected, x.ap_dict['AP12'])

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error1)
    def test_input1(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Network coordinates must be integers')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error2)
    def test_input2(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Channel must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error3)
    def test_input3(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Channel must be between 1 and 11')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error4)
    def test_input4(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Power must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error5)
    def test_input5(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Frequency must be "2.4, 6, 5"')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error6)
    def test_input6(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Frequency must be "2.4, 6, 5"')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error7)
    def test_input7(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Network wifi standard must be in format "WiFi{number}"')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error8)
    def test_input8(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Incorrect Supports standards: Must be either "false" or "true".')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error9)
    def test_input9(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Incorrect Supports standards: Must be either "false" or "true".')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error10)
    def test_input10(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Incorrect Supports standards: Must be either "false" or "true".')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error11)
    def test_input11(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Coverage must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error12)
    def test_input12(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Device_limit must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error13)
    def test_input13(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            x = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Minimal RSSI must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error14)
    def test_input14(self, mock_file):
        with self.assertRaises(ValueError) as e:
            x = RoamingSimulator(mock_file)
        self.assertIn('Unrecognized line:', str(e.exception))


if __name__ == '__main__':
    unittest.main()

