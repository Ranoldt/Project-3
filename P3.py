import math
import pickle

""""
binary file (used in the call methods of AP and clientObj class) (used in the call method of RS, for 
with open('name.dat', 'wb') as f:
    pickle.dump(self.log, f)
"""


class RoamingSimulator:
    def __init__(self, path):
        self.file = open(path,'r')
        self.client_dict = {}
        self.ap_dict = {}
        self.moves = []
        self.initalize_functions()

    def initalize_functions(self):
        self.file_read()
        print('files done')
        self.access_controller()
        print('controllers done')
        self.connect(list(self.client_dict.values()))
        print('inital connection done')
        self.iterate_moves()

    def file_read(self):
        for line in self.file:
            line = line.split()
            print(line)
            if line[0] == 'AP':
                self.ap_dict[line[1]] = AccessPoints(*line[1:])
            elif line[0] == 'CLIENT':
                self.client_dict[line[1]] = ClientObj(*line[1:])
            elif line[0] == 'MOVE':
                self.moves.append(line[1:])

    def find_distance(self, obj1, obj2):
        x1, y1 = obj1.coord
        x2, y2 = obj2.coord

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def is_overlap(self, ap1, ap2):
        overlap_radius = ap1.coverage + ap2.coverage
        distance = self.find_distance(ap1, ap2)
        if overlap_radius > distance:
            return True
        else:
            return False

    def access_controller(self):
        self.aclog = []
        step = 1
        ap_lst = list(self.ap_dict.values())
        for ap1 in ap_lst:
            ap1_copy = ap1
            channels = [ap1.channel]
            while True:
                changed = False
                for ap2 in ap_lst:
                    if ap1 is not ap2 and ap1.channel == ap2.channel and self.is_overlap(ap1, ap2):
                        for channel in [11, 6, 1]:
                            if channel not in channels:
                                channels.append(channel)
                                ap1.channel = channel
                                changed = True
                                break
                        else:
                            new_channel = ap1.channel - 1 if ap1.channel > 1 else 2
                            ap1.channel = new_channel
                            channels.append(ap1.channel)
                            changed = True
                if not changed:
                    break
            if ap1 != ap1_copy:
                self.aclog.append(f'Step {step}: AC REQUIRES {ap1.name} TO CHANGE CHANNEL TO {ap1.channel}')
                step += 1
            ap_lst = list(self.ap_dict.values())

    def iterate_moves(self):
        for move in self.moves:
            self.client_dict[move[0]].client_move(move[1:])
            self.connect([self.client_dict[move[0]]], True)

    def __call__(self, name):
        obj_dict = {**self.ap_dict, **self.client_dict}
        if name == 'AC':
            return self.aclog
        return obj_dict[name].__call__()

    def connect(self, cl, roam=None):
        for client_obj in cl:
            connectable_ap = []
            for ap_name, ap_obj in self.ap_dict.items():
                cl_rssi = self.calculate_rssi(ap_obj, self.find_distance(client_obj, ap_obj))
                print(cl_rssi)
                if cl_rssi < client_obj.minimal_rssi:
                    continue
                elif ap_obj.minimal_rssi:
                    if cl_rssi < ap_obj.minimal_rssi:
                        continue
                connectable_ap.append(ap_obj)
            if len(connectable_ap) == 0:
                if client_obj.connected:
                    client_obj.disconnect_to_ap()
                    client_obj.connected = None
                return
            connectable_ap = self.configure_connections(client_obj, connectable_ap)
            if connectable_ap[0].name == client_obj.connected:
                return
            for ap in connectable_ap:
                if client_obj.connect_to_ap(ap, roam):
                    ap.add_client(client_obj)
                    break

    def configure_connections(self, cl, lst):
        def sorting_connections(ap):
            return (
                self.sort_channel(ap),
                -max(ap.frequency),
                -ap.power,
                self.sort_standards(ap,cl),
                ap.standard[1] < cl.standard[1]
            )
        lst = sorted(lst, key=sorting_connections)
        return lst

    def sort_standards(self, ap, cl):
        matches = [x == y for x, y in zip(ap.suppports, cl.supports)]
        match_count = sum(matches)

        return (
            -match_count,
            -int(matches[2]),
        )

    def sort_channel(self, ap):
        if ap.channel == 11:
            return 0
        elif ap.channel == 6:
            return 1
        elif ap.channel == 1:
            return 2
        else:
            return 3

    def calculate_rssi(self, ap, distance):
        print('distamce', distance)
        print('ap', ap.name)
        print('frequency', ap.frequency[0])
        return ap.power - 20 * math.log(distance, 10) - 20 * math.log(ap.frequency[0] * 1000, 10) - 32.44

    def binary_AC(self):
        with open('AccessController.dat', 'wb') as file:
            pickle.dump(self.aclog, file)


class AccessPoints(RoamingSimulator):
    def __init__(self, *parameters):
        if len(parameters) == 13:
            self.minimal_rssi = -int(parameters[-1])
        else:
            self.minimal_rssi = None
        self.name = parameters[0]
        self.coord = (int(parameters[1]), int(parameters[2]))
        self.channel = int(parameters[3])
        self.power = int(parameters[4])
        self.frequency = tuple(map(float, (parameters[5].split('/'))))
        self.standard = (parameters[6], int(parameters[6][4:]))
        self.supports = (parameters[7], parameters[8], parameters[9])
        self._11k, self._11v, self._11r = self.supports
        self.coverage = int(parameters[10])
        self.device_limit = int(parameters[11])
        self.clients = []
        self.log = []
        self.step = 0

    def add_client(self, client, roam=None):
        if len(self.clients) < self.device_limit:
            if roam:
                if self._11r == 'true':
                    self.log.append(f'Step {self.step}: {client.name} FAST ROAM TO {self.name}')
                else:
                    self.log.append(f'Step {self.step}: {client.name} ROAM TO {self.name}')
            self.clients.append(client)
            self.log.append(
                f'Step {self.step}: {client.name} CONNECT LOCATION {client.coord[0]} {client.coord[1]} {client.standard[0]} {client.speed} {client._11k} {client._11v} {client._11r}')
        elif roam:
            self.log.append(f'Step {self.step}: {client.name} TRIED {self.name} BUT WAS DENIED')

    def remove_client(self, client):
        self.log.append(
            f'Step {self.step}: {client.name} DISCONNECTS AT LOCATION {client.coord[0]} {client.coord[1]}')
        self.clients.remove(client)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.channel == other.channel

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.coord},{self.channel},{self.power},{self.frequency},{self.standard[0]},{self.supports},{self.coverage},{self.device_limit},{self.minimal_rssi})'

    def __call__(self):
        return self.log


class ClientObj(RoamingSimulator):
    def __init__(self, *parameters):
        self.name = parameters[0]
        self.coord = (int(parameters[1]), int(parameters[2]))
        self.standard = (parameters[3], int(parameters[3][4:]))
        self.speed = tuple(map(float, (parameters[4].split('/'))))
        self.supports = (parameters[5], parameters[6], parameters[7])
        self._11k, self._11v, self._11r = self.supports
        self.minimal_rssi = -int(parameters[8])
        self.log = []
        self.step = 1
        self.connected = None

    def client_move(self, move):
        self.coord = (int(move[0]), int(move[1]))

    def connect_to_ap(self, ap, roam=None):
        if len(ap.clients) < ap.device_limit:
            if roam:
                self.log.append(f'Step {self.step}: CLIENT ROAM FROM {self.connected} TO {ap.name}')
                self.step += 1
                self.disconnect_to_ap()
                ap.remove_client(self)
            self.connected = ap.name
            self.signal_strength = RoamingSimulator.calculate_rssi(ap, RoamingSimulator.find_distance(self, ap))
            self.log.append(f'Step {self.step}: CLIENT CONNECT TO {ap.name} WITH SIGNAL STRENGTH {self.signal_strength}')
            self.step += 1
            return True
        elif roam:
            self.log.append(f'Step {self.step}: CLIENT ROAM DENIED')
            self.step += 1
            return False
        return False

    def disconnect_to_ap(self):
        self.log.append(f'Step {self.step}: CLIENT DISCONNECT FROM {self.connected} WITH SIGNAL STRENGTH {self.signal_strength}')
        self.step += 1

    def __call__(self):
        return self.log

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.coord},{self.standard[0]},{self.speed},{self.supports},{self.minimal_rssi})'


if __name__ == '__main__':
    x = RoamingSimulator('input.txt')
    print(x.client_dict)
    print(x.ap_dict)
