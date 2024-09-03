from network_entity import NetworkEntity


class AccessPoints(NetworkEntity):
    def __init__(self, *parameters):
        super().__init__(*parameters[:3], parameters[6], parameters[5], *parameters[7:9], *parameters[9::3])
        assert parameters[3].isdigit(), 'Channel must be an integer'
        assert 0 < int(parameters[3]) <= 11, 'Channel must be between 1 and 11'
        assert parameters[4].isdigit(), 'Power must be an integer'
        assert parameters[10].isdigit(), 'Coverage must be an integer'
        assert parameters[11].isdigit(), 'Device_limit must be an integer'
        self.channel = int(parameters[3])
        self.power = int(parameters[4])
        self.coverage = int(parameters[10])
        self.device_limit = int(parameters[11])
        self.clients = []
        self.step = 1

    def add_client(self, client, roam=None):
        if len(self.clients) < self.device_limit:
            if roam:
                if self.supports_11r == 'true':
                    self.log_action(f'Step {self.step}: {client.name} FAST ROAM TO {self.name}')
                else:
                    self.log_action(f'Step {self.step}: {client.name} ROAM TO {self.name}')
            self.clients.append(client)
            self.log_action(
                f'Step {self.step}: {client.name} CONNECT LOCATION {client.coord[0]} {client.coord[1]} {client.wifi_standard} {client.frequency_str} {client.supports_11k} {client.supports_11v} {client.supports_11r}')
            return True
        else:
            self.log_action(f'Step {self.step}: {client.name} TRIED {self.name} BUT WAS DENIED')
            return False

    def remove_client(self, client):
        self.log_action(
            f'Step {self.step}: {client.name} DISCONNECTS AT LOCATION {client.x} {client.y}')
        client.x, client.y = client.coord[0], client.coord[1]
        self.clients.remove(client)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.coord[0]},{self.coord[1]},{self.channel},{self.power},{self.frequency_str},{self.wifi_standard},{self.supports[0]},{self.supports[1]},{self.supports[2]},{self.coverage},{self.device_limit},{self.minimal_rssi})'
