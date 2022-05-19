import json
from pathlib import Path
from common.stream import Stream
from common.task import Job
from common.util import traverse_dir

if __name__ == '__main__':

    pcap_path = "/opt/pcaps/small_tests"

    joy_job = Job()
    s = joy_job.do_job_joy(pcap_path)

    zeek_job = Job()
    k = zeek_job.do_job_zeek(pcap_path)

    print("===== Summary =====")
    print("Target: %s" % pcap_path)
    print(json.dumps(s, indent=4))
    print(json.dumps(k, indent=4))