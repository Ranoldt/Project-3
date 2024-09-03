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
            'AP AP2 20 20 6 20 2.4/5 WiFi6 true true false 50 4\n'
            'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
            'MOVE Client1 25 25')

roaming2 = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
            'AP AP2 20 20 6 20 2.4/5 WiFi6 true true true 50 4\n'
            'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
            'MOVE Client1 25 25')

roaming3 = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
            'AP AP2 20 20 6 20 2.4/5 WiFi6 true true true 50 1\n'
            'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
            'CLIENT Client2 21 21 WiFi4 2.4/5 true true true 110\n'
            'MOVE Client1 25 25')

roaming4 = ('AP AP1 0 0 6 20 2.4/5 WiFi6 true true true 50 4\n'
            'AP AP2 20 20 6 20 2.4/5 WiFi6 true true true 50 1\n'
            'AP AP3 40 40 6 20 2.4/5 WiFi6 true true true 50 1\n'
            'AP AP4 60 60 6 20 2.4/5 WiFi6 true true true 50 1\n'
            'CLIENT Client1 5 5 WiFi4 2.4/5 true true true 110\n'
            'MOVE Client1 21 21\n'
            'MOVE Client1 42 42\n'
            'MOVE Client1 63 63\n')

ap_evaluation = ('AP AP1 0 0 6 18 2.4 WiFi5 true true true 0 10 75\n'
                 "AP AP2 7 7 6 18 2.4 WiFi6 true false false 0 10 75\n"
                 "AP AP3 6 6 6 18 2.4 WiFi6 false true false 0 10\n"
                 'AP AP4 5 5 6 15 2.4 WiFi6 true false true 0 10\n'
                 "AP AP5 4 4 11 20 2.4 WiFi7 false false true 0 5\n"
                 "AP AP6 3 3 11 20 2.4 WiFi7 true true true 0 10\n"
                 "AP AP7 2 2 11 20 2.4 WiFi7 false true true 0 5\n"
                 "AP AP8 1 1 11 21 2.4 WiFi7 false true true 0 5\n"
                 "AP AP9 8 8 11 21 5 WiFi7 false true true 0 5\n"
                 "AP AP10 12 12 1 21 6 WiFi7 false true true 0 5\n"
                 "AP AP11 13 13 6 21 6 WiFi7 false true true 0 5\n"
                 "AP AP12 14 14 11 21 6 WiFi7 false true true 0 5\n"
                 "CLIENT Client1 10 10 WiFi6 2.4/5 false true true 1000\n")

input_error1 = 'AP AP1 w w 6 18 2.4 WiFi5 true true true 0 10 75\n'
input_error2 = 'AP AP1 1 1 w 18 2.4 WiFi5 true true true 0 10 75\n'
input_error3 = 'AP AP1 1 1 15 18 2.4 WiFi5 true true true 0 10 75\n'
input_error4 = 'AP AP1 1 1 6 w 2.4 WiFi5 true true true 0 10 75\n'
input_error5 = 'AP AP1 1 1 6 18 w WiFi5 true true true 0 10 75\n'
input_error6 = 'AP AP1 1 1 6 18 7 WiFi5 true true true 0 10 75\n'
input_error7 = 'AP AP1 1 1 6 18 2.4 5 true true true 0 10 75\n'
input_error8 = 'AP AP1 1 1 6 18 2.4 WiFi5 w true true 0 10 75\n'
input_error9 = 'AP AP1 1 1 6 18 2.4 WiFi5 true w true 0 10 75\n'
input_error10 = 'AP AP1 1 1 6 18 2.4 WiFi5 true true w 0 10 75\n'
input_error11 = 'AP AP1 1 1 6 18 2.4 WiFi5 true true true w 10 75\n'
input_error12 = 'AP AP1 1 1 6 18 2.4 WiFi5 true true true 0 w 75\n'
input_error13 = 'AP AP1 1 1 6 18 2.4 WiFi5 true true true 0 10 w\n'

input_error14 = 'AFIFI DJIFJIJIOFNHIO JFIOJ FIPJPOWJPOFKOPJ EFPOJPOF\n'

simulation = ('AP AP1 0 0 11 20 5 WiFi7 true true true 20 10 120\n'
              'AP AP2 10 10 11 23 2.4/5 WiFi6 true false false 20 10 100\n'
              'AP AP3 50 50 6 19 6 WiFi8 true true true 20 10 130\n'
              'AP AP4 60 60 6 25 5 WiFi8 false true false 20 10 100\n'
              'AP AP5 200 200 11 30 6 WiFi7 false true true 20 10 100\n'
              'CLIENT Client1 5 5 WiFi6 2.4/5 true true true 110\n'
              'CLIENT Client2 6 6 WiFi6 2.4/5 true false false 110\n'
              'CLIENT Client3 55 55 WiFi6 2.4/5 false false false 110\n'
              'CLIENT Client4 65 65 WiFi6 6 false false true 110\n'
              'CLIENT Client5 201 201 WiFi6 2.4/5 false true true 110\n'
              'MOVE Client1 54 54\n'
              'MOVE Client2 64 64\n'
              'MOVE Client3 4 4\n'
              'MOVE Client4 5 5\n'
              'MOVE Client5 300 300\n')















