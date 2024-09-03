import math


class NetworkEntity:
    def __init__(self, name,x,y, wifi_standard, frequency, supports_11k, supports_11v, supports_11r, minimal_rssi=None):
        assert supports_11r in ('true', 'false') and supports_11v in ('true', 'false') and supports_11k in ('true', 'false'), 'Incorrect Supports standards: Must be either "false" or "true".'
        assert x.isdigit() and y.isdigit(), 'Network coordinates must be integers'
        assert 'WiFi' in wifi_standard and wifi_standard[4:].isdigit() , 'Network wifi standard must be in format "WiFi{number}"'
        assert all(x in ('2.4', '5', '6') for x in frequency.split('/')) and len(frequency.split('/')) < 4, 'Frequency must be "2.4, 6, 5"'
        if minimal_rssi:
            assert minimal_rssi.isdigit(), 'Minimal RSSI must be an integer'
        self.name = name
        self.x = x
        self.y = y
        self.coord = (int(x), int(y))
        self.frequency_str = frequency
        self.wifi_standard = wifi_standard
        self.standard = int(wifi_standard[4:])
        self.supports = (supports_11k, supports_11v, supports_11r)
        self.supports_11k = supports_11k
        self.supports_11v = supports_11v
        self.supports_11r = supports_11r
        self.minimal_rssi = -int(minimal_rssi) if minimal_rssi is not None else None
        self.frequency = list(map(float,self.frequency_str.split('/')))
        self.log = []
        self.step = 1

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.coord}, {self.frequency_str}, {self.wifi_standard}, {self.supports})'

    def calculate_rssi(self, ap, distance):
        speeds = [speed for speed in self.frequency and ap.frequency]
        frequency = max(speeds) if len(speeds) > 0 else max(ap.frequency)
        return ap.power - 20 * math.log(distance, 10) - 20 * math.log(frequency * 1000, 10) - 32.44

    def find_distance(self, obj2):
        x1, y1 = self.coord
        x2, y2 = obj2.coord

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def log_action(self, message):
        self.log.append(message)
        self.step += 1

    def __call__(self):
        return self.log
