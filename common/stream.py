class Stream:
    def __init__(self):
        self.src_ip = ""
        self.src_port = 0
        self.dest_ip = ""
        self.dest_port = 0

    def setup(self, src_ip, src_port, dest_ip, dest_port):
        self.src_ip = src_ip
        self.src_port = src_port
        self.dest_ip = dest_ip
        self.dest_port = dest_port