from client import ClientObj
from access_point import AccessPoints
import math
import pickle

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

if __name__ == '__main__':
    x = RoamingSimulator('input.txt')
    print(x.client_dict)
    print(x.ap_dict)

