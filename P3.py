from math import sqrt


class AccessController:
    def __init__(self, ap_dict):
        self.AP_dict = ap_dict
        self.log = []
        self.step = 0

    def find_distance(self, ap1, ap2):
        x1, y1 = ap1.coord
        x2, y2 = ap2.coord

        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance

    def is_overlap(self, ap1, ap2):
        overlap_radius = ap1.coverage + ap2.coverage
        distance = self.find_distance(ap1, ap2)
        if overlap_radius > distance:
            return True
        else:
            return False

    def compare_aps(self):
        ap_lst = list(self.AP_dict.values())
        for ap1 in ap_lst:
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
            self.log.append(f'Step {self.step}: AC REQUIRES {ap1.apName} TO CHANGE CHANNEL TO {ap1.channel}')
            ap_lst = list(self.AP_dict.values())

class AccessPoints:
    def __init__(self, *parameters):
        self.parameters = parameters
        if len(parameters) == 13:
            self.minimal_rssi = parameters[-1]
        else:
            self.minimal_rssi = None
        self.apName = parameters[0]
        self.coord = (int(parameters[1]), int(parameters[2]))
        self.channel = int(parameters[3])
        self.power = parameters[4]
        self.frequency = parameters[5]
        self.standard = parameters[6]
        self.supports = (parameters[7],parameters[8],parameters[9])
        self._11k, self._11v, self._11r = self.supports
        self.coverage = int(parameters[10])
        self.device_limit = parameters[11]
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def __len__(self):
        return len(self.clients)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.apName},{self.coord},{self.channel},{self.power},{self.frequency},{self.standard},{self.supports},{self.coverage},{self.device_limit},{self.minimal_rssi})'


class ClientObj:
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

    def client_move(self,move):
        self.coord = (int(move[0]), int(move[1]))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.clientName},{self.coord},{self.standard},{self.speed},{self.supports},{self.minimal_rssi})'




class FileManager:
    def __init__(self, path):
        self.path = path
        self.client_dict = {}
        self.AP_dict = {}
    def __enter__(self):
        self.file = open(self.path, 'r')
        return self.file
    def line_process(self):
        for line in self.file:
            line = line.split()
            if line[0] == 'AP':
                self.AP_dict[line[1]] = AccessPoints(line[1:])
            elif line[0] == 'CLIENT':
                self.client_dict[line[1]] = ClientObj(line[1:])
            elif line[0] == 'MOVE':
                self.client_dict[line[1]].client_move((line[2], line[3]))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

class AP:
    def __init__(self, *parameters):
        self.channel = int(parameters[0])
        self.coord = (int(parameters[1]), int(parameters[2]))
        self.coverage = int(parameters[3])
    def __repr__(self):
        return f'{self.__class__.__name__}({self.channel},{self.coord},{self.coverage})'

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


    print(client_dict)
    print(AP_dict)