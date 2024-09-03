from network_entity import NetworkEntity


class AccessController:
    def __init__(self, ap_dict, client_dict):
        self.ap_dict = ap_dict
        self.client_dict = client_dict
        self.log = []
        self.step = 1
        self.change_channels()

    def change_channels(self):
        ap_lst = list(self.ap_dict.values())
        for ap1 in ap_lst:
            ap1_copy = ap1.channel
            channels = [ap1.channel]
            iterated = False
            while True:
                channel_count = len(channels)
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
                            if not iterated:
                                ap1.channel = channels[0]
                                iterated = True
                            new_channel = ap1.channel - 1 if ap1.channel > 1 else 2
                            ap1.channel = new_channel
                            if ap1.channel not in channels:
                                channels.append(ap1.channel)
                            changed = True
                if not changed:
                    break
                if len(channels) == channel_count:
                    raise ValueError(f'AP has run out channels:{ap1}')
            if ap1.channel != ap1_copy:
                self.log.append(f'Step {self.step}: AC REQUIRES {ap1.name} TO CHANGE CHANNEL TO {ap1.channel}')
                self.step += 1
            ap_lst = list(self.ap_dict.values())

    def is_overlap(self, ap1, ap2):
        overlap_radius = ap1.coverage + ap2.coverage
        distance = NetworkEntity.find_distance(ap1, ap2)
        if overlap_radius > distance:
            return True
        else:
            return False

    def __call__(self):
        cl_dict = {cl.name: cl.log for cl in self.client_dict.values()}
        ap_dict = {ap.name: ap.log for ap in self.ap_dict.values()}
        _dict = {'AccessController': self.log, **ap_dict, **cl_dict}
        return _dict
