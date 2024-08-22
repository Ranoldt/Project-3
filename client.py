
class ClientObj():
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
        from roaming_simulator import RoamingSimulator

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
