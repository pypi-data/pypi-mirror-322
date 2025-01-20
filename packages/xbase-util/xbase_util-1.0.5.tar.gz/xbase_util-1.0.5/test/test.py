import csv

import pandas as pd
from scapy.utils import rdpcap

from xbase_util.packet_util import has_templates_injection, has_sql_injection, has_dir_penetration, \
    has_code_injection_or_execute
from xbase_util.pcap_util import reassemble_session_pcap, reassemble_tcp_pcap

if __name__ == '__main__':
    packets_scapy=rdpcap('code_injection.pcap')
    # skey = f"10.255.76.196:49942"
    skey = f'10.255.76.196:50077'
    tcp=reassemble_tcp_pcap(packets_scapy)
    all_packets = reassemble_session_pcap(tcp, skey,
                                          session_id="id")
    for packet in all_packets:
        res=has_code_injection_or_execute([packet['req_header'], packet['req_body']])
        print(res)
    pd.DataFrame(all_packets).to_csv('all_packets.csv')