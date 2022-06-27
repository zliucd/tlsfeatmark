"""
MIT license
Copyright (C) 2022 Zhi Liu<zliucd66@gmail.com>

task.py
This file is part of TLSfeatmark, a testing package for TLS analytics. See LICENSE for more information.
"""

from pathlib import Path
from time import perf_counter

from common.util import traverse_dir
from parser.joyparser import parse_pcap_joy
from parser.zeekparser import parse_pcap_zeek


class Job:
    """
    Job class
    """

    def __init__(self, config):
        """
        Job instance initialization
        Args:
            config: config instance in dict
        """
        self.config = config

    def do_job_joy(self, pcap_path):
        """
        Analyze pcaps from pcap_path using Joy
        Args:
            pcap_path: pcap file or dir path

        Returns:
            analysis results in dict

        """

        tls_total = 0
        cert_total = 0
        elapsed_total = 0.0

        results = dict()
        results["job"] = dict()
        results["task"] = []
        i = 0

        print("[INFO]Joy begins to analyze %s" % pcap_path)

        pcap_files = traverse_dir(pcap_path)
        for pcap_file in pcap_files:
            task = Task(config=self.config)
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

        results["job"]["tool"] = "joy"
        results["job"]["pcap_path"] = pcap_path
        results["job"]["pcap_num"] = i
        results["job"]["tls_total"] = tls_total
        results["job"]["cert_total"] = cert_total
        results["job"]["elapsed_total"] = round(elapsed_total, 2)

        return results

    def do_job_zeek(self, pcap_path):
        """
        Analyze pcaps from pcap_path using Zeek
        Args:
            pcap_path: pcap file or dir path

        Returns:
            analysis results in dict

        """

        tls_total = 0
        cert_total = 0
        elapsed_total = 0.0

        results = dict()
        results["job"] = dict()
        results["task"] = []
        i = 0

        print("[INFO]Zeek begins to analyze %s" % pcap_path)

        pcap_files = traverse_dir(pcap_path)
        for pcap_file in pcap_files:
            task = Task(config=self.config)

            tls_num, cert_num, elapsed = task.do_task_zeek(pcap_file)

            d = dict()

            name = Path(pcap_file).name
            d["name"] = name
            d["tls_num"] = tls_num
            d["cert_num"] = cert_num
            d["elapsed"] = round(elapsed, 4)

            results["task"].append(d)

            tls_total += tls_num
            cert_total += cert_num
            elapsed_total += elapsed
            i += 1

        results["job"]["tool"] = "zeek"
        results["job"]["pcap_path"] = pcap_path
        results["job"]["pcap_num"] = i
        results["job"]["tls_total"] = tls_total
        results["job"]["cert_total"] = cert_total
        results["job"]["elapsed_total"] = round(elapsed_total, 2)

        return results


class Task:
    """
    Pcap analysis task
    """

    def __init__(self, config):
        """
        Task instance initialization
        Args:
            config: config dict
        """
        self.config = config

    def do_task_joy(self, pcap_file):
        """
        Analyze a single pcap file using Joy
        Args:
            pcap_file: pcap file path

        Returns:
            tls_num: TLS stream number
            cert_num: certificate number
            elapsed: analysis time
        """

        p = Path(pcap_file)

        start_timer = perf_counter()
        tls_num, cert_num = parse_pcap_joy(pcap_file)

        end_timer = perf_counter()
        elapsed = end_timer - start_timer
        elapsed = round(elapsed, 2)

        if self.config["enable_task_print"] == "on":
            print("[Joy]%s, TLS: %d, cert: %d, elapsed: %f" % (p.name, tls_num, cert_num, elapsed))

        return tls_num, cert_num, elapsed

    def do_task_zeek(self, pcap_file):
        """
        Analyze a single pcap file using Zeek
        Args:
            pcap_file: pcap file path

        Returns:
            tls_num: TLS stream number
            cert_num: certificate number
            elapsed: analysis time
        """

        p = Path(pcap_file)

        start_timer = perf_counter()
        tls_num, cert_num = parse_pcap_zeek(pcap_file)

        end_timer = perf_counter()
        elapsed = end_timer - start_timer
        elapsed = round(elapsed, 2)

        if self.config["enable_task_print"] == "on":
            print("[Zeek]%s, TLS: %d, cert: %d, elapsed: %f" % (p.name, tls_num, cert_num, elapsed))

        return tls_num, cert_num, elapsed
