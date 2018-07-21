import time

class Time_Controler:

    def __init__(self):
        self.start_time = time.clock()
        self.period = 6  #max call per second to the server
        self.marge = 0.2

    def END_time(self):
        return time.time()

    def Duration_time(self):
        return self.END_time() - self.start_time

    def Spike_Sender(self):
        time.sleep(1/(self.period * (1 - self.marge)))
        return True
