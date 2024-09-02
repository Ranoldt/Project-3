initial_connection = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 10\n'
                      'CLIENT Client1 10 10 WiFi6 2.4/5 true true true 110\n')

initial_connection2 = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 10\n'
                       'CLIENT Client1 10 10 WiFi6 2.4/5 true true true 110\n'
                       'AP AP2 100 100 6 20 2.4/5 WiFi6 true true true 50 10\n'
                       'CLIENT Client2 99 99 WiFi4 2.4/5 true true true 110\n')

client_limit = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
                'CLIENT Client1 10 10 WiFi6 2.4/5 true true true 110\n'
                'CLIENT Client2 9 9 WiFi4 2.4/5 true true true 110\n'
                'CLIENT Client3 8 8 WiFi6 2.4/5 true true true 110\n'
                'CLIENT Client4 7 7 WiFi4 2.4/5 true true true 110\n'
                'CLIENT Client5 6 6 WiFi4 2.4/5 true true true 110\n')

access_controller = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
                     'AP AP2 10 10 6 20 2.4/5 WiFi6 true true true 50 4\n'
                     'AP AP3 20 20 6 20 2.4/5 WiFi6 true true true 50 4\n'
                     'AP AP4 30 30 6 20 2.4/5 WiFi6 true true true 50 4\n')

ac_no_overlap = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
                 'AP AP2 100 100 6 20 2.4/5 WiFi6 true true true 50 4\n'
                 'AP AP3 200 200 6 20 2.4/5 WiFi6 true true true 50 4\n')

move_inside = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
               'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
               'MOVE Client1 10 10')

move_outside = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
                'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
                'MOVE Client1 20 20')

roaming1 = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
            'AP AP2 20 20 6 20 2.4/5 WiFi6 true true true 50 4\n'
            'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
            'MOVE Client1 25 25')

