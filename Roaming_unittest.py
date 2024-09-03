import unittest
import store_inputs as s
from unittest.mock import mock_open, patch
from roaming_simulator import RoamingSimulator


class TestRoamingSimulator(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=s.initial_connection)
    def test_initial_connection1(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP1'])
        self.assertEqual(len(simulator.ap_dict['AP1'].clients), 1)
        self.assertIs(simulator.ap_dict['AP1'].clients[0], simulator.client_dict['Client1'])
        self.assertEqual(simulator.AC(), {'AccessController': [], 'AP1': ['Step 1: Client1 CONNECT LOCATION 10 10 WiFi6 2.4/5 true true true'], 'Client1': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 109.42970004336019']})

    @patch('builtins.open', new_callable=mock_open, read_data=s.initial_connection2)
    def test_initial_connection2(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client2'].connected, simulator.ap_dict['AP2'])
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP1'])
        self.assertIn(simulator.client_dict['Client1'],simulator.ap_dict['AP1'].clients)
        self.assertIn(simulator.client_dict['Client2'],simulator.ap_dict['AP2'].clients)
        self.assertEqual(simulator.AC(), {'AccessController': [], 'AP1': ['Step 1: Client1 CONNECT LOCATION 10 10 WiFi6 2.4/5 true true true'], 'AP2': ['Step 1: Client2 CONNECT LOCATION 99 99 WiFi4 2.4/5 true true true'], 'Client1': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 109.42970004336019'], 'Client2': ['Step 1: CLIENT CONNECT TO AP2 WITH SIGNAL STRENGTH 89.42970004336019']})

    @patch('builtins.open', new_callable=mock_open, read_data=s.client_limit)
    def test_AP_client_limit(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP1'])
        self.assertEqual(simulator.client_dict['Client2'].connected, simulator.ap_dict['AP1'])
        self.assertEqual(simulator.client_dict['Client3'].connected, simulator.ap_dict['AP1'])
        self.assertEqual(simulator.client_dict['Client4'].connected, simulator.ap_dict['AP1'])
        self.assertIn(simulator.client_dict['Client1'], simulator.ap_dict['AP1'].clients)
        self.assertIn(simulator.client_dict['Client2'], simulator.ap_dict['AP1'].clients)
        self.assertIn(simulator.client_dict['Client3'], simulator.ap_dict['AP1'].clients)
        self.assertIn(simulator.client_dict['Client4'], simulator.ap_dict['AP1'].clients)
        self.assertEqual(simulator.client_dict['Client5'].connected, None)
        self.assertNotIn(simulator.client_dict['Client5'], simulator.ap_dict['AP1'].clients)
        self.assertEqual(simulator.AC(),{'AccessController': [], 'AP1': ['Step 1: Client1 CONNECT LOCATION 10 10 WiFi6 2.4/5 true true true', 'Step 2: Client2 CONNECT LOCATION 9 9 WiFi4 2.4/5 true true true', 'Step 3: Client3 CONNECT LOCATION 8 8 WiFi6 2.4/5 true true true', 'Step 4: Client4 CONNECT LOCATION 7 7 WiFi4 2.4/5 true true true', 'Step 5: Client5 TRIED AP1 BUT WAS DENIED'], 'Client1': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 109.42970004336019'], 'Client2': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 108.51455023214668'], 'Client3': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 107.49149978319906'], 'Client4': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 106.33166084364532'], 'Client5': []})

    @patch('builtins.open', new_callable=mock_open, read_data=s.access_controller)
    def test_access_controller(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.ap_dict['AP1'].channel, 11)
        self.assertEqual(simulator.ap_dict['AP2'].channel, 1)
        self.assertEqual(simulator.ap_dict['AP3'].channel, 5)
        self.assertEqual(simulator.ap_dict['AP4'].channel, 6)
        self.assertEqual(simulator.AC.log, ['Step 1: AC REQUIRES AP1 TO CHANGE CHANNEL TO 11', 'Step 2: AC REQUIRES AP2 TO CHANGE CHANNEL TO 1', 'Step 3: AC REQUIRES AP3 TO CHANGE CHANNEL TO 5'])

    @patch('builtins.open', new_callable=mock_open, read_data= s.ac_no_overlap)
    def test_no_overlap(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.ap_dict['AP1'].channel, 6)
        self.assertEqual(simulator.ap_dict['AP2'].channel, 6)
        self.assertEqual(simulator.ap_dict['AP3'].channel, 6)

    @patch('builtins.open', new_callable=mock_open, read_data = s.move_inside)
    def test_move_within_coverage(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP1'])
        self.assertEqual(simulator.client_dict['Client1'].coord, (10,10))

    @patch('builtins.open', new_callable=mock_open, read_data=s.move_outside)
    def test_move_outside_coverage(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].coord, (20,20))
        self.assertEqual(simulator.client_dict['Client1'].connected, None)
        self.assertEqual(simulator.AC(), {'AccessController': [], 'AP1': ['Step 1: Client1 CONNECT LOCATION 5 5 WiFi4 2.4/5 true true true', 'Step 2: Client1 DISCONNECTS AT LOCATION 5 5'], 'Client1': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 103.40910013008056', 'Step 2: CLIENT DISCONNECT FROM AP1 WITH SIGNAL STRENGTH 115.45029995663981']})

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming1)
    def test_roaming_to_ap(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP2'])
        self.assertEqual(simulator.client_dict['Client1'].coord, (25, 25))
        self.assertNotIn(simulator.client_dict['Client1'], simulator.ap_dict['AP1'].clients)
        self.assertIn(simulator.client_dict['Client1'], simulator.ap_dict['AP2'].clients)
        self.assertIn('Step 1: Client1 ROAM TO AP2', simulator.ap_dict['AP2'].log)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming2)
    def test_fast_roaming(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP2'])
        self.assertEqual(simulator.client_dict['Client1'].coord, (25, 25))
        self.assertNotIn(simulator.client_dict['Client1'], simulator.ap_dict['AP1'].clients)
        self.assertIn(simulator.client_dict['Client1'], simulator.ap_dict['AP2'].clients)
        self.assertIn('Step 1: Client1 FAST ROAM TO AP2', simulator.ap_dict['AP2'].log)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming3)
    def test_denied_roaming(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, None)
        self.assertEqual(simulator.client_dict['Client1'].coord, (25, 25))
        self.assertNotIn(simulator.client_dict['Client1'], simulator.ap_dict['AP2'].clients)
        self.assertIn('Step 2: Client1 TRIED AP2 BUT WAS DENIED', simulator.ap_dict['AP2'].log)

    @patch('builtins.open', new_callable=mock_open, read_data=s.roaming4)
    def test_multiple_movement(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].coord, (63, 63))
        self.assertEqual(simulator.ap_dict['AP1'].log,['Step 1: Client1 CONNECT LOCATION 5 5 WiFi4 2.4/5 true true true', 'Step 2: Client1 DISCONNECTS AT LOCATION 5 5'])
        self.assertEqual(simulator.ap_dict['AP2'].log,['Step 1: Client1 FAST ROAM TO AP2', 'Step 2: Client1 CONNECT LOCATION 21 21 WiFi4 2.4/5 true true true', 'Step 3: Client1 DISCONNECTS AT LOCATION 21 21'])
        self.assertEqual(simulator.ap_dict['AP3'].log,['Step 1: Client1 FAST ROAM TO AP3', 'Step 2: Client1 CONNECT LOCATION 42 42 WiFi4 2.4/5 true true true', 'Step 3: Client1 DISCONNECTS AT LOCATION 42 42'])
        self.assertEqual(simulator.ap_dict['AP4'].log,['Step 1: Client1 FAST ROAM TO AP4', 'Step 2: Client1 CONNECT LOCATION 63 63 WiFi4 2.4/5 true true true'])

    @patch('builtins.open', new_callable=mock_open, read_data=s.ap_evaluation)
    def test_AP_evaluation(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.client_dict['Client1'].connected, simulator.ap_dict['AP12'])

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error1)
    def test_input1(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Network coordinates must be integers')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error2)
    def test_input2(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Channel must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error3)
    def test_input3(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Channel must be between 1 and 11')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error4)
    def test_input4(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Power must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error5)
    def test_input5(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Frequency must be "2.4, 6, 5"')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error6)
    def test_input6(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Frequency must be "2.4, 6, 5"')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error7)
    def test_input7(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Network wifi standard must be in format "WiFi{number}"')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error8)
    def test_input8(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Incorrect Supports standards: Must be either "false" or "true".')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error9)
    def test_input9(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Incorrect Supports standards: Must be either "false" or "true".')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error10)
    def test_input10(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Incorrect Supports standards: Must be either "false" or "true".')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error11)
    def test_input11(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Coverage must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error12)
    def test_input12(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Device_limit must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error13)
    def test_input13(self, mock_file):
        with self.assertRaises(AssertionError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertEqual(str(e.exception), 'Minimal RSSI must be an integer')

    @patch('builtins.open', new_callable=mock_open, read_data=s.input_error14)
    def test_input14(self, mock_file):
        with self.assertRaises(ValueError) as e:
            simulator = RoamingSimulator(mock_file)
        self.assertIn('Unrecognized line:', str(e.exception))

    @patch('builtins.open', new_callable=mock_open, read_data=s.simulation)
    def test_simulation(self, mock_file):
        simulator = RoamingSimulator(mock_file)
        self.assertEqual(simulator.AC(), {'AccessController': ['Step 1: AC REQUIRES AP1 TO CHANGE CHANNEL TO 6', 'Step 2: AC REQUIRES AP3 TO CHANGE CHANNEL TO 11'], 'AP1': ['Step 1: Client1 CONNECT LOCATION 5 5 WiFi6 2.4/5 true true true', 'Step 2: Client1 DISCONNECTS AT LOCATION 5 5', 'Step 3: Client3 FAST ROAM TO AP1', 'Step 4: Client3 CONNECT LOCATION 4 4 WiFi6 2.4/5 false false false', 'Step 5: Client4 FAST ROAM TO AP1', 'Step 6: Client4 CONNECT LOCATION 5 5 WiFi6 6 false false true'], 'AP2': ['Step 1: Client2 CONNECT LOCATION 6 6 WiFi6 2.4/5 true false false', 'Step 2: Client2 DISCONNECTS AT LOCATION 6 6'], 'AP3': ['Step 1: Client1 FAST ROAM TO AP3', 'Step 2: Client1 CONNECT LOCATION 54 54 WiFi6 2.4/5 true true true'], 'AP4': ['Step 1: Client3 CONNECT LOCATION 55 55 WiFi6 2.4/5 false false false', 'Step 2: Client4 CONNECT LOCATION 65 65 WiFi6 6 false false true', 'Step 3: Client2 ROAM TO AP4', 'Step 4: Client2 CONNECT LOCATION 64 64 WiFi6 2.4/5 true false false', 'Step 5: Client3 DISCONNECTS AT LOCATION 55 55', 'Step 6: Client4 DISCONNECTS AT LOCATION 65 65'], 'AP5': ['Step 1: Client5 CONNECT LOCATION 201 201 WiFi6 2.4/5 false true true', 'Step 2: Client5 DISCONNECTS AT LOCATION 201 201'], 'Client1': ['Step 1: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 103.40910013008056', 'Step 2: CLIENT ROAM FROM AP1 TO AP3', 'Step 3: CLIENT DISCONNECT FROM AP1 WITH SIGNAL STRENGTH 124.07757523981955', 'Step 4: CLIENT CONNECT TO AP3 WITH SIGNAL STRENGTH 104.05452479087192'], 'Client2': ['Step 1: CLIENT CONNECT TO AP2 WITH SIGNAL STRENGTH 98.47089986991944', 'Step 2: CLIENT ROAM FROM AP2 TO AP4', 'Step 3: CLIENT DISCONNECT FROM AP2 WITH SIGNAL STRENGTH 121.07757523981955', 'Step 4: CLIENT CONNECT TO AP4 WITH SIGNAL STRENGTH 96.47089986991944'], 'Client3': ['Step 1: CLIENT CONNECT TO AP4 WITH SIGNAL STRENGTH 98.40910013008056', 'Step 2: CLIENT ROAM FROM AP4 TO AP1', 'Step 3: CLIENT DISCONNECT FROM AP4 WITH SIGNAL STRENGTH 119.39346058348418', 'Step 4: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 101.47089986991944'], 'Client4': ['Step 1: CLIENT CONNECT TO AP4 WITH SIGNAL STRENGTH 98.40910013008056', 'Step 2: CLIENT ROAM FROM AP4 TO AP1', 'Step 3: CLIENT DISCONNECT FROM AP4 WITH SIGNAL STRENGTH 119.23695383324505', 'Step 4: CLIENT CONNECT TO AP1 WITH SIGNAL STRENGTH 103.40910013008056'], 'Client5': ['Step 1: CLIENT CONNECT TO AP5 WITH SIGNAL STRENGTH 81.01332496431267', 'Step 2: CLIENT DISCONNECT FROM AP5 WITH SIGNAL STRENGTH 121.01332496431267']})


if __name__ == '__main__':
    unittest.main()

