import os

class Logger(object):

    def __init__(self):
        self.filename = "/home/ubuntu/apps/physmappython/physmap.log"

    def log(self, msg):
        with open(self.filename, 'a') as f:
            f.write("%s%s" % (msg, "\n"))