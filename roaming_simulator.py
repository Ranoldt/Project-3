from client import ClientObj
from access_point import AccessPoints
from access_controller import AccessController
import math
import pickle

class RoamingSimulator:
    def __init__(self, path):
        self.file = open(path,'r')
        self.client_dict = {}
        self.ap_dict = {}
        self.moves = []
        self.initialize_functions()

    def initialize_functions(self):
        self.file_read()
        self.AC = AccessController(self.ap_dict, self.client_dict)
        self.find_connections(list(self.client_dict.values()))
        self.iterate_moves()

    def file_read(self):
        for line in self.file:
            line = line.split()
            if len(line) != 0:
                if line[0] == 'AP':
                    self.ap_dict[line[1]] = AccessPoints(*line[1:])
                elif line[0] == 'CLIENT':
                    self.client_dict[line[1]] = ClientObj(*line[1:])
                elif line[0] == 'MOVE':
                    self.moves.append(line[1:])
                else:
                    raise ValueError('Unrecognized line:', line)

    def find_distance(self, obj1, obj2):
        x1, y1 = obj1.coord
        x2, y2 = obj2.coord

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1)**2)

    def iterate_moves(self):
        for move in self.moves:
            self.client_dict[move[0]].client_move(move[1:])
            self.find_connections([self.client_dict[move[0]]], True)

    def find_connections(self, cl, roam=None):
        for client_obj in cl:
            connectable_ap = []
            for ap_name, ap_obj in self.ap_dict.items():
                cl_rssi = RoamingSimulator.calculate_rssi(client_obj, ap_obj, self.find_distance(client_obj, ap_obj))
                if cl_rssi < client_obj.minimal_rssi:
                    continue
                elif ap_obj.minimal_rssi:
                    if cl_rssi < ap_obj.minimal_rssi:
                        continue
                connectable_ap.append(ap_obj)
            self.connection_protocol(client_obj, connectable_ap, roam)

    def connection_protocol(self, client_obj, connectable_ap, roam):
        if not connectable_ap:
            if client_obj.connected:
                self.disconnect_protocol(client_obj)
            return
        connectable_ap = self.configure_connections(client_obj, connectable_ap)
        if connectable_ap[0] is client_obj.connected:
            return
        for ap in connectable_ap:
            client_obj.connect_to_ap(ap, roam)
            if ap.add_client(client_obj, roam):
                break
        else:
            if client_obj.connected:
                self.disconnect_protocol(client_obj)

    def disconnect_protocol(self, client_obj):
        client_obj.connected.remove_client(client_obj)
        client_obj.disconnect_to_ap()

    def configure_connections(self, cl, lst):
        def sorting_connections(ap):
            return (
                ap.standard < cl.standard,
                self.sort_standards(ap,cl),
                -ap.power,
                -max(ap.frequency),
                self.sort_channel(ap)
            )
        lst = sorted(lst, key=sorting_connections)
        return lst

    def sort_standards(self, ap, cl):
        matches = [x == y for x, y in zip(ap.supports, cl.supports)]
        match_count = sum(matches)
        true_count = sum(1 for x,y in zip(ap.supports, cl.supports) if x == 'true' and y == 'true')

        return (
            -match_count,
            -int(matches[2]),
            -true_count
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

    @staticmethod
    def calculate_rssi(client, ap, distance):
        speeds = [speed for speed in client.frequency and ap.frequency]
        frequency = max(speeds) if len(speeds) > 0 else max(ap.frequency)
        return ap.power - 20 * math.log(distance, 10) - 20 * math.log(frequency * 1000, 10) - 32.44

    def __call__(self, name):
        obj_dict = {**self.ap_dict, **self.client_dict, 'AccessController': self.AC}
        with open(f'{name}.dat', 'wb') as f:
            pickle.dump(obj_dict[name].__call__(), f)
