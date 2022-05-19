import os

def traverse_dir(pcap_path):
    """
    Traverse dir, get all pcaps absolute paths
    :param pcap_path: pcap path, either file or dir name
    :return: pcaps paths
    """

    pcap_files = []

    if os.path.isfile(pcap_path):
        pcap_files.append(pcap_path)
    elif os.path.isdir(pcap_path):
        for root, dir_names, file_names in os.walk(pcap_path):
            for f in file_names:
                if f[0:2] != "._" and f[-5:] == ".pcap":
                    pcap_files.append(os.path.join(root, f))

    return pcap_files