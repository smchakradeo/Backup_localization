class datapoint:
    def __init__(self, time, anchor, power, distance):
        self.time = time
        self.anchor = anchor
        self.power = power
        self.distance = distance

    def get_dp(self):
        dp = [self.time, self.anchor, self.power, self.distance]
        return dp

