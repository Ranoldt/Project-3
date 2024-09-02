from network_entity import NetworkEntity


class ClientObj(NetworkEntity):
    def __init__(self, *parameters):
        super().__init__(*parameters)
        self.step = 1
        self.connected = None

    def client_move(self, move):
        self.coord = (int(move[0]), int(move[1]))

    def connect_to_ap(self, ap, roam=None):
        if len(ap.clients) < ap.device_limit:
            if roam:
                self.log_action(f'Step {self.step}: CLIENT ROAM FROM {self.connected.name} TO {ap.name}')
                self.connected.remove_client(self)
                self.disconnect_to_ap()
            self.connected = ap
            self.signal_strength = self.calculate_rssi(ap, self.find_distance(ap))
            self.log_action(f'Step {self.step}: CLIENT CONNECT TO {ap.name} WITH SIGNAL STRENGTH {-self.signal_strength}')
        elif roam:
            self.log_action(f'Step {self.step}: CLIENT ROAM DENIED')

    def disconnect_to_ap(self):
        self.log_action(f'Step {self.step}: CLIENT DISCONNECT FROM {self.connected.name} WITH SIGNAL STRENGTH {-self.signal_strength}')
        self.connected = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.coord},{self.wifi_standard},{self.frequency},{self.supports},{self.minimal_rssi})'


if __name__ == '__main__':
    x = ['Client1', '10', '10', 'WiFi6', '2.4/5', 'true', 'true', 'true', '73']
    client = ClientObj(*x)
    print(client)