# TLSfeatmark

### What is Tlsfeatmark
```Tlsfeatmark``` is a benchmark tool for TLS analytics using **Joy** and **Zeek**. It generates
nice JSON output on several statistics for each pcap and all pcaps analyzed:
 - the number of TCP stream found
 - the number of TLS stream found
 - the number of certificates found
 - the elapsed time of analysis
 
### Sample output

```
===== Summary =====
{
    "cpu": "11th Gen Intel(R) Core(TM) i7-11700K @ 3.60GHz",
    "os": "Linux 4.18.0-348.2.1.el8_5.x86_64",
    "time": "2022-06-27 13:43:03",
    "joy": {
        "job": {
            "tool": "joy",
            "pcap_path": "/home/dev/tlsfeatmark/pcaps/small_pcaps",
            "pcap_num": 5,
            "tls_total": 323,
            "cert_total": 294,
            "elapsed_total": 0.32
        },
        "task": [
            {
                "name": "2021-01-13-Emotet-epoch-2-infection-traffic-with-Trickbot-gtag-mor13-2.pcap",
                "tls_num": 46,
                "cert_num": 78,
                "elapsed": 0.06
            },
            {
                "name": "2021-01-04-Emotet-infection-with-Trickbot-traffic.pcap",
                "tls_num": 10,
                "cert_num": 10,
                "elapsed": 0.04
            }
            ... # skip several other tasks
        ]
    },
    "zeek": {
        "job": {
            "tool": "zeek",
            "pcap_path": "/home/dev/tlsfeatmark/pcaps/small_pcaps",
            "pcap_num": 5,
            "tls_total": 323,
            "cert_total": 477,
            "elapsed_total": 1.06
        },
        "task": [
            {
                "name": "2021-01-13-Emotet-epoch-2-infection-traffic-with-Trickbot-gtag-mor13-2.pcap",
                "tls_num": 46,
                "cert_num": 84,
                "elapsed": 0.23
            },
            {
                "name": "2021-01-04-Emotet-infection-with-Trickbot-traffic.pcap",
                "tls_num": 10,
                "cert_num": 15,
                "elapsed": 0.17
            },
            ...        
            # skip several other tasks
        ]
    }
}

```


### Environment
```Tlsfeatmark``` relies on Joy and Zeek, and they work well on Linux and Mac OSX.

 - Linux: Centos8/Ubuntu20.04, tested
 - Mac: x86/M1, tested 
 - Windows: untested 

### How to install 

1. Install Joy

see Joy [official documentation](https://github.com/cisco/joy/wiki/Installation) for installation.

2. Install Zeek

see Zeek [official documentation](https://docs.zeek.org/en/master/install.html) for installation.

3. Install tlsfeatmark

```pip install tlsfeatmark```

### How to use
```Tlsfeatmark``` is easy to use once Joy and Zeek are installed.

1. Configure ```pcap_path``` in ```config.txt```

```pcap_path``` is the pcap file or dir containing pcaps to be analyzed.

```pcap_path``` supports absolute and relative path. For relative path (relative to ```main.py```), use ```./``` as prefix, for example, ```./pcaps/small_pcaps```.

2. Run ```main.py```

3. View results in ```output``` folder.

### License
```Tlsfeatmark``` is under MIT license, see LICENSE for more information.