import os

from common.util import traverse_dir
from pathlib import Path


def parse_zeek_output(pcap):
    """
    Parse feature file generated by Joy, output number of TLS streams and certs,
    :param feat_path:
    :return:
    """

    tls_num = 0
    cert_num = 0
    lines = []

    try:
        f = open("ssl.log")
        lines = f.readlines()

        for line in lines:
            if line[0] == "#":
                pass
            else:
                tls_num += 1

    except:
        pass

    return tls_num, cert_num

def run_zeek_command(pcap_path):

    p = Path(pcap_path)

    cmd_str = "zeek -Cr %s" %pcap_path
    ret = os.system(cmd_str)

    if ret == 0:
        print("%s processed by Zeek success" % p.name)
    else:
        print("%s processed by Zeek error" % p.name)

    return ret


def parse_pcap_zeek(pcap_path):
    """
    Invoke zeek to parse pcaps in pcap_dir and save feature files in output dir
    :param pcap_path: input dir where pcaps are saved
    :return:
    """

    run_zeek_command(pcap_path)
    tls_num, cert_num = parse_zeek_output(pcap_path)

    os.system("rm *.log")   # remove all log for current pcap file

    return tls_num, cert_num