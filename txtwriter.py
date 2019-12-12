
import os

class TxtWriter:
    def __init__(self, txt):
        self.name = txt
        self.fout = open(txt, 'w')

    def __del__(self):
        self.close()

    def close(self):
        if not self.fout.closed:
            self.fout.close()

    def write(self, var):
        self.fout.write(str(var)+'\n')

    def archive(self):
        self.close()
        if os.path.isfile(self.name):
            os.system('bzip2 '+self.name)
