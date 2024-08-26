from network_entity import NetworkEntity


class AccessController:
    def __init__(self, ap_dict):
        self.ap_dict = ap_dict
        self.log = []
        self.step = 1
        self.access_controller()

    def access_controller(self):
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
                self.log.append(f'Step {self.step}: AC REQUIRES {ap1.name} TO CHANGE CHANNEL TO {ap1.channel}')
                self.step += 1
            ap_lst = list(self.ap_dict.values())

    @staticmethod
    def is_overlap(self, ap1, ap2):
        overlap_radius = ap1.coverage + ap2.coverage
        distance = NetworkEntity.find_distance(ap1, ap2)
        if overlap_radius > distance:
            return True
        else:
            return False

    def __call__(self):
        return self.log
