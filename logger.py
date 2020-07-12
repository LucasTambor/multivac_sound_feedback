class Logger(object):
    def __init__(self, name):
        self.name = name
        self.header = "[{}] ->".format(self.name)

    def log(self, msg):
        print("{} {}".format(self.header, msg), flush=True)

