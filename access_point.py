
class AccessPoints():
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