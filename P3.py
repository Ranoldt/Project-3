import math


class RoamingSimulator:
    def __init__(self, path):
        self.file = path
        self.client_dict = {}
        self.ap_dict = {}
        self.moves = []
        self.initalizeFunctions()

    def initalizeFunctions(self):
        self.file_read()
        self.access_controller()

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
                self.aclog.append(f'Step {step}: AC REQUIRES {ap1.apName} TO CHANGE CHANNEL TO {ap1.channel}')
                step += 1
            ap_lst = list(self.ap_dict.values())

    def iterate_moves(self):
        for move in self.moves:
            self.client_dict[move[0]].client_move(move[1:])

    def __call__(self, name):
        obj_dict = {**self.ap_dict, **self.client_dict}
        if name == 'AC':
            return self.aclog
        return obj_dict[name].__call__()


"""
develop move method
"""


class AccessPoints(RoamingSimulator):
    def __init__(self, *parameters):
        if len(parameters) == 13:
            self.minimal_rssi = parameters[-1]
        else:
            self.minimal_rssi = None
        self.apName = parameters[0]
        self.coord = (int(parameters[1]), int(parameters[2]))
        self.channel = int(parameters[3])
        self.power = int(parameters[4])
        self.frequency = map(int, (parameters[5].split('/')))
        self.standard = parameters[6]
        self.supports = (parameters[7], parameters[8], parameters[9])
        self._11k, self._11v, self._11r = self.supports
        self.coverage = int(parameters[10])
        self.device_limit = int(parameters[11])
        self.clients = []
        self.log = []
        self.step = 0

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def __len__(self):
        return len(self.clients)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.channel == other.channel

    def __repr__(self):
        return f'{self.__class__.__name__}({self.apName},{self.coord},{self.channel},{self.power},{self.frequency},{self.standard},{self.supports},{self.coverage},{self.device_limit},{self.minimal_rssi})'

    def __call__(self):
        return self.log


class ClientObj(RoamingSimulator):
    def __init__(self, *parameters):
        self.clientName = parameters[0]
        self.coord = (int(parameters[1]), int(parameters[2]))
        self.standard = parameters[3]
        self.speed = parameters[4]
        self.supports = (parameters[5], parameters[6], parameters[7])
        self._11k, self._11v, self._11r = self.supports
        self.minimal_rssi = parameters[8]
        self.log = []
        self.step = 0

    def client_move(self, move):
        self.coord = (int(move[0]), int(move[1]))

    def calculate_rssi(ap, distance):
        return ap.power - 20 * math.log10(distance) - 20 * math.log(ap.frequency) - 32.44

    def connect_to_ap(self, ap):
        if self.calculate_rssi(ap, RoamingSimulator.find_distance(self, ap)) < self.minimal_rssi:
            pass

    def __call__(self):
        return self.log

    def __repr__(self):
        return f'{self.__class__.__name__}({self.clientName},{self.coord},{self.standard},{self.speed},{self.supports},{self.minimal_rssi})'


if __name__ == '__main__':
    client_dict = {}
    AP_dict = {}
    file = open('input.txt', 'r')
    lines = file.readlines()
    for line in lines:
        line = line.split()
        if line[0] == 'AP':
            AP_dict[line[1]] = AccessPoints(*line[1:])
        elif line[0] == 'CLIENT':
            client_dict[line[1]] = ClientObj(*line[1:])

