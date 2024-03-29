"""
MIT license
Copyright (C) 2022 Zhi Liu<zliucd66@gmail.com>

main.py
This file is part of TLSfeatmark, a testing package for TLS analytics. See LICENSE for more information.
"""

import datetime
import json
import os
from pathlib import Path

from common.task import Job
from common.util import setup, get_platform_info

if __name__ == '__main__':

    print("===== TLSfeatmark - a testing package for TLS analytics using Joy and Zeek, v0.1 =====")

    config = setup("config.txt")
    if config == None:
        print("[ERROR]Setup fail, see error messages")
        exit(0)

    pcap_path = config["pcap_path"]
    abs_path = ""
    if pcap_path[0:2] == "./":
        abs_path = os.path.join(os.getcwd(), pcap_path[2:])
    else:
        abs_path = pcap_path

    joy_job = Job(config)
    joy_results = joy_job.do_job_joy(abs_path)

    zeek_job = Job(config)
    zeek_results = zeek_job.do_job_zeek(abs_path)

    print("===== Summary =====")
    results = dict()

    cpuinfo, osinfo = get_platform_info()
    results["cpu"] = cpuinfo
    results["os"] = osinfo

    e = datetime.datetime.now()
    t = e.strftime(e.strftime("%Y-%m-%d %H:%M:%S"))
    results["time"] = t

    results["joy"] = joy_results
    results["zeek"] = zeek_results

    output = json.dumps(results, indent=4)
    print(output)

    curr_time = datetime.datetime.now()
    fmt_time = curr_time.strftime("%Y-%m-%d_%H:%M:%S")

    fname = Path(pcap_path).stem + "_" + fmt_time + ".json"
    fpath = os.path.join(os.getcwd(), "output", fname)

    f = open(fpath, "w")
    f.write(output)

    print("[INFO]Testing results have been written to %s" % fpath)
    print("\n===== TLSfeatmark done =====")