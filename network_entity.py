import math


class NetworkEntity:
    def __init__(self, name,x,y, wifi_standard, frequency, supports_11k, supports_11v, supports_11r, minimal_rssi=None):
        self.name = name
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

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def log_action(self, message):
        self.log.append(message)
        self.step += 1

    def __call__(self):
        return self.log
