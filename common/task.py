from time import perf_counter
from parser.joyparser import parse_pcap_joy
from parser.zeekparser import parse_pcap_zeek
from common.util import traverse_dir
from pathlib import Path

class Job:
    def __init__(self):
        self.pcap_path = ""
        self.tls_total = 0
        self.cert_total = 0
        self.elapsed_total = 0.0

    def do_job_joy(self, pcap_path):

        pcap_files = traverse_dir(pcap_path)

        print("[Joy job]Begin to analyze %s " % pcap_files)
        for pcap_file in pcap_files:
            task = Task(pcap_path=pcap_file)

            tls_num, cert_num, elapsed = task.do_task_joy(pcap_file)

            self.tls_total += tls_num
            self.cert_total += cert_num
            self.elapsed_total += elapsed

        self.elapsed_total = round(self.elapsed_total, 2)
        s = "[Joy job]Finished, TLS: %d, cert: %d, elapsed: %2f" % (self.tls_total, self.cert_total, self.elapsed_total)
        print(s)

        return s

    def do_job_zeek(self, pcap_path):

        pcap_files = traverse_dir(pcap_path)

        print("[Zeek Job]Begin to analyze %s " % pcap_files)
        for pcap_file in pcap_files:
            task = Task(pcap_path=pcap_file)

            tls_num, cert_num, elapsed = task.do_task_zeek(pcap_file)

            self.tls_total += tls_num
            self.cert_total += cert_num
            self.elapsed_total += elapsed

        self.elapsed_total = round(self.elapsed_total, 2)
        s = "[Zeek Job]Finished, TLS: %d, cert: %d, elapsed: %f" % (self.tls_total, self.cert_total, self.elapsed_total)


        print(s)
        return s


class Task:
    def __init__(self, pcap_path):
        self.tls_num = 0
        self.cert_num = 0
        self.start_timer = None
        self.end_timer = None
        self.elapsed = 0.0

    def do_task_joy(self, pcap_path):

        p = Path(pcap_path)
        # print("[Task]Begin to analyze %s " % p.name)

        self.start_timer = perf_counter()
        tls_num, cert_num = parse_pcap_joy(pcap_path)

        self.end_timer = perf_counter()
        elapsed = self.end_timer - self.start_timer
        self.elapsed = round(elapsed, 2)

        print("[Task]Finished, TLS: %d, cert: %d, elapsed: %f" % (tls_num, cert_num, elapsed))

        return tls_num, cert_num, elapsed


    def do_task_zeek(self, pcap_path):

        p = Path(pcap_path)
        # print("[Task]Begin to analyze %s " % p.name)

        self.start_timer = perf_counter()
        tls_num, cert_num = parse_pcap_zeek(pcap_path)

        self.end_timer = perf_counter()
        elapsed = self.end_timer - self.start_timer
        self.elapsed = round(elapsed, 2)

        print("[Task]Finished, TLS: %d, cert: %d, elapsed: %f" % (tls_num, cert_num, elapsed))

        return tls_num, cert_num, elapsed

