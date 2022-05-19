from time import perf_counter
from parser.joyparser import parse_pcap_joy
from parser.zeekparser import parse_pcap_zeek
from common.util import traverse_dir
from pathlib import Path

class Job:
    def __init__(self):
        pass

    def do_job_joy(self, pcap_path):

        tls_total = 0
        cert_total = 0
        elapsed_total = 0.0


        results = dict()
        results["job"] = dict()
        results["task"] = []
        i = 0

        pcap_files = traverse_dir(pcap_path)
        for pcap_file in pcap_files:
            task = Task(pcap_path=pcap_file)

            tls_num, cert_num, elapsed = task.do_task_joy(pcap_file)

            d = dict()
            d["name"] = Path(pcap_file).name
            d["tls_num"] = tls_num
            d["cert_num"] = cert_num
            d["elapsed"] = round(elapsed, 4)

            results["task"].append(d)

            tls_total += tls_num
            cert_total += cert_num
            elapsed_total += elapsed

            i += 1

        results["job"]["pcap_num"] = i
        results["job"]["tls_total"] = tls_total
        results["job"]["cert_total"] = cert_total
        results["job"]["elapsed_total"] = round(elapsed_total, 2)

        return results

    def do_job_zeek(self, pcap_path):

        tls_total = 0
        cert_total = 0
        elapsed_total = 0.0

        results = dict()
        results["job"] = dict()
        results["task"] = []
        i = 0

        pcap_files = traverse_dir(pcap_path)
        for pcap_file in pcap_files:
            task = Task(pcap_path=pcap_file)

            tls_num, cert_num, elapsed = task.do_task_zeek(pcap_file)

            d = dict()
            d["name"] = Path(pcap_file).name
            d["tls_num"] = tls_num
            d["cert_num"] = cert_num
            d["elapsed"] = round(elapsed, 4)

            results["task"].append(d)

            tls_total += tls_num
            cert_total += cert_num
            elapsed_total += elapsed

            i += 1

        results["job"]["pcap_num"] = i
        results["job"]["tls_total"] = tls_total
        results["job"]["cert_total"] = cert_total
        results["job"]["elapsed_total"] = round(elapsed_total, 2)

        return results



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


