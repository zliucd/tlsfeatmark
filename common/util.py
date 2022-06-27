"""
MIT license
Copyright (C) 2022 Zhi Liu<zliucd66@gmail.com>

task.py
This file is part of TLSfeatmark, a testing package for TLS analytics. See LICENSE for more information.
"""

import os, configparser
import cpuinfo, platform

def setup(config_path):
    """
    Parse config file and check if Joy and Zeek have been installed
    Args:
        config_path: config file path

    Returns:
        dict: config object, return None if error occurs
    """

    d = read_config(config_path)
    if d == None:
        return None

    # check if Joy and Zeek are in-place to use
    ret = check_tools_exists()
    if ret != 0:
        return None

    print("[INFO]Setup success")

    return d


def read_config(config_path):
    """
    Read config from config path
    Args:
        config_path: config path

    Returns:
        config instance
    """

    d = None

    try:
        config = configparser.ConfigParser()
        config.read(config_path)

        d = dict()
        d["pcap_path"] = config["default"]["pcap_path"]
        d["enable_task_print"] = config["default"]["enable_task_print"]
    except Exception as e:
        print("[ERROR]Config file not not exist or parsing error, msg: %s" % str(e))
        d = None

    return d


def get_platform_info():
    """
    Get cpu and os information
    Returns:
        cpu, osinfo
    """

    cpu = cpuinfo.get_cpu_info()["brand_raw"]
    osinfo = platform.system() + " " + platform.release()

    return cpu, osinfo


def check_tools_exists():
    """
    Check if Joy and Zeek have benn installed
    Returns:
        0 for Joy and Zeek are installed, otherwise -1
    """
    ret1 = check_joy_exists()
    ret2 = check_zeek_exists()

    if ret1 == 0 and ret2 == 0:
        return 0
    elif ret1 != 0:
        print("[ERROR]Joy is not installed, see Joy installation documentation https://github.com/cisco/joy/wiki/Installation")
    elif ret2 != 0:
        print("[ERROR]Zeek is not installed, see Zeek installation documentation https://docs.zeek.org/en/master/install.html")

    return -1


def check_joy_exists():
    """
    Check if Joy has been installed
    Returns:
        0 for installed otherwise -1
    """
    ret = os.popen('joy --help').read()

    if "command not found" in ret:
        return -1

    return 0


def check_zeek_exists():
    """
    Check if Zeek has been installed
    Returns:
        0 for installed otherwise -1
    """
    ret = os.popen('zeek --version').read()

    if "command not found" in ret:
        print("[ERROR]Zeek is not installed, visit https://docs.zeek.org/en/master/install.html")
        return -1

    return 0


def traverse_dir(pcap_path):
    """
    Traverse dir, get all pcaps absolute paths.
    If it's file, return a list with a single file.
    Error occurs if the path does not exist.
    Args:
        pcap_path: pcap file or dir path

    Returns:
        a list of pcap files paths
    """

    pcap_files = []

    if os.path.isfile(pcap_path):
        pcap_files.append(pcap_path)
    elif os.path.isdir(pcap_path):
        for root, dir_names, file_names in os.walk(pcap_path):
            for f in file_names:
                if f[0:2] != "._" and f[-5:] == ".pcap":
                    pcap_files.append(os.path.join(root, f))
    else:
        print("[ERROR]Check pcap path, which does not exist. Current given path: %s" % pcap_path)
        exit(0)

    return pcap_files
