import time

class Time_Controler:

    def __init__(self):
        self.start_time = time.clock()
        self.period = 6  #max call per second to the server
        self.marge = 0.2

    def Ask_time(self):
        return time.clock()

    def Duration_time(self):
        return self.Ask_time() - self.start_time

    def Spike_Sender(self):
        time.sleep(1/(self.period * (1 - self.marge)))
        return True

    def Sleep_Time(self, time_):
        time.sleep(time_)
        return True
