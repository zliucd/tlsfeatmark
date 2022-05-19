import os, json
from tempfile import NamedTemporaryFile

from common.stream import Stream
from common.util import traverse_dir
from pathlib import Path

def parse_joy_output(feat_path):
    """
    Parse feature file generated by Joy, output number of TLS streams and certs,
    :param feat_path:
    :return:
    """

    p = Path(feat_path)

    f = open(feat_path)
    lines = f.readlines()

    tls_num = 0
    cert_num = 0

    lines = lines[1:]   #skip first line
    for line in lines:
        j = json.loads(line)
        if "tls" in j:
            s = j["tls"]

            tls_num += 1
            if "s_cert" in s:
                cert_num += len(s["s_cert"])

    return tls_num, cert_num

def run_joy_command(pcap_path):

    p = Path(pcap_path)
    f = NamedTemporaryFile("w+t", delete=False)

    cmd_str = "joy tls=1 dist=1 ssh=1 tls=1 bidir=1 fpx=1 %s | gunzip > %s" % (pcap_path, f.name)
    ret = os.system(cmd_str)

    if ret == 0:
        print("%s processed by Joy success" % p.name)
    else:
        print("%s processed by Joy error" % p.name)

    return f.name

def parse_pcap_joy(pcap_path):

    output = run_joy_command(pcap_path)
    tls_num, cert_num = parse_joy_output(output)

    return tls_num, cert_num