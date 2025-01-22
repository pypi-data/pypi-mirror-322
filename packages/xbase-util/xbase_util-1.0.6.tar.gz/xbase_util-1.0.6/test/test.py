from scapy.contrib.igmp import IGMP
from scapy.contrib.igmpv3 import IGMPv3gr, IGMPv3, IGMPv3mr, IGMPv3mq, IGMPv3mra
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.tls.record import TLS
from scapy.packet import Raw
from scapy.utils import rdpcap
from protocol_parser import *

if __name__ == '__main__':
    pcaps = rdpcap("flags.pcap")
    session = {
        'common_protocols': [],
        # 'common_packets_src': 0,
        # 'common_packets_dst': 0,
        'common_packets': len(pcaps),
        'common_bytes': 0,
        'common_first_packet_time': int(pcaps[0].time*1000),
        'common_last_packet_time': int(pcaps[-1].time*1000),
        'common_tcp_flag_ack': 0,
        'common_tcp_flag_syn_ack': 0,
        'common_tcp_flag_psh': 0,
        'common_tcp_flag_syn': 0,
        'common_tcp_flag_fin': 0,
        'common_tcp_flag_rst': 0,
        'common_tcp_flag_urg': 0,
        'common_ip_protocol': [],
    }
    for index, pkt in enumerate(pcaps):
        if IP in pkt and index == 0 or index == 1:
            ip = pkt[IP]
            session['common_ip_protocol'].append(ip.proto)
            if 'common_sip' not in session:
                session['common_sip'] = ip.src
                session['common_spt'] = ip.sport if hasattr(ip, 'sport') else 0
                session['common_dip'] = ip.dst
                session['common_dpt'] = ip.dport if hasattr(ip, 'dport') else 0
            if ip.proto == 89:
                session['common_protocols'].append('ospf')
        if TCP in pkt:
            session['common_protocols'].append('tcp')
            flags = pkt[TCP].flags
            if "A" == f"{flags}":
                session['common_tcp_flag_ack'] += 1
            if "SA" == f"{flags}":
                session['common_tcp_flag_syn_ack'] += 1
            if "S" == f"{flags}":
                session['common_tcp_flag_syn'] += 1
            if "P" in flags:
                session['common_tcp_flag_psh'] += 1
            if "F" in flags:
                session['common_tcp_flag_fin'] += 1
            if "R" in flags:
                session['common_tcp_flag_rst'] += 1
            if "U" in flags:
                session['common_tcp_flag_urg'] += 1
            if Raw in pkt:
                raw_data = pkt[Raw].load
                if TLS in pkt:
                    session['common_protocols'].append('tls')
                    if parse_tls_http2(pkt[TLS]):
                        session['common_protocols'].append('http2')
                if parse_http_http(raw_data):
                    session['common_protocols'].append('http')
                if parse_tcp_tls(raw_data):
                    session['common_protocols'].append('tls')
                if parse_tcp_redis(raw_data):
                    session['common_protocols'].append('redis')
                if parser_tcp_oracle(raw_data):
                    session['common_protocols'].append('oracle')
                if parse_tcp_ftp(raw_data):
                    session['common_protocols'].append('ftp')
                if parse_tcp_ssh(raw_data):
                    session['common_protocols'].append('ssh')
                if parse_tcp_pop3(raw_data):
                    session['common_protocols'].append('pop3')
                if parse_tcp_mysql(raw_data):
                    session['common_protocols'].append('mysql')
                if parse_tcp_stmp(raw_data):
                    session['common_protocols'].append('smtp')
                if parse_tcp_postgresql(raw_data):
                    session['common_protocols'].append('postgresql')
                if parse_tcp_nfs(raw_data):
                    session['common_protocols'].append('nfs')
                if parse_tcp_splunk(raw_data):
                    session['common_protocols'].append('splunk')
                if parse_tcp_kafka(raw_data):
                    session['common_protocols'].append('kafka')
                if parse_tcp_zookeeper(raw_data):
                    session['common_protocols'].append('zookeeper')
                if parse_tcp_smb(raw_data):
                    session['common_protocols'].append('smb')
                if parse_tcp_decerpc(raw_data):
                    session['common_protocols'].append('dcerpc')
                if parse_tcp_mongo(raw_data):
                    session['common_protocols'].append('mongo')
                if parse_tcp_x11(raw_data):
                    session['common_protocols'].append('x11')
                if parse_tcp_vnc(raw_data):
                    session['common_protocols'].append('vnc')
                if parse_tcp_ldap(raw_data):
                    session['common_protocols'].append('ldap')
                if parse_tcp_telnet(session['common_dpt'], raw_data):
                    session['common_protocols'].append("telnet")
                if parse_tcp_imap(raw_data):
                    session['common_protocols'].append("imap")
                if parse_tcp_dnp3(raw_data):
                    session['common_protocols'].append("dnp3")
                if parse_tcp_krb5(raw_data):
                    session['common_protocols'].append("krb5")
                if parse_thrift(raw_data):
                    session['common_protocols'].append("thrift")
                if parse_tcp_syslog(raw_data):
                    session['common_protocols'].append("syslog")
                if parse_tcp_bittorrent(raw_data):
                    session['common_protocols'].append("bittorrent")
                if parse_dnp3(raw_data):
                    session['common_protocols'].append("dnp3")
                if parse_tcp_stun(raw_data):
                    session['common_protocols'].append("stun")
                if parse_tcp_memcached(raw_data):
                    session['common_protocols'].append("memcached")
                if parse_tcp_mqtt(raw_data):
                    session['common_protocols'].append("mqtt")
                if parse_tcp_rdp(raw_data):
                    session['common_protocols'].append("rdp")
                if parse_tcp_rmi(raw_data):
                    session['common_protocols'].append("rmi")
                if parse_tcp_pjl(raw_data):
                    session['common_protocols'].append("pjl")
                if parse_tcp_bgp(session['common_dpt'], raw_data):
                    session['common_protocols'].append("bgp")
                if parse_tcp_rtsp(raw_data):
                    session['common_protocols'].append("rtsp")
                if parse_tcp_gh0st(raw_data):
                    session['common_protocols'].append("gh0st")
                if parse_tcp_jabber(raw_data):
                    session['common_protocols'].append("jabber")
                if parse_tcp_socket(raw_data):
                    session['common_protocols'].append("socket")
                if parse_tcp_http2(raw_data):
                    session['common_protocols'].append("http2")
            if parse_tcp_udp(pkt[TCP].dport):
                session['common_protocols'].append('dns')  #tcp的dns
        elif UDP in pkt:
            session['common_spt'] = pkt[UDP].sport
            session['common_dpt'] = pkt[UDP].dport
            session['common_protocols'].append('udp')
            if Raw in pkt:
                raw_data = pkt[Raw].load
                if parse_udp_nfs(raw_data):
                    session['common_protocols'].append('nfs')
                if parse_udp_dnp3(raw_data):
                    session['common_protocols'].append("dnp3")
                if parse_udp_krb5(raw_data):
                    session['common_protocols'].append("krb5")
                if parse_udp_ntp(session['common_spt'], session['common_dpt'], raw_data):
                    session['common_protocols'].append("ntp")
                if parse_udp_dhcpv6(session['common_dpt'], raw_data):
                    session['common_protocols'].append("dhcpv6")
                if parse_udp_snmap(raw_data, session['common_spt'], session['common_dpt']):
                    session['common_protocols'].append("snmap")
                if parse_udp_dns(pkt[UDP].dport):
                    session['common_protocols'].append('dns')
                if parse_udp_llmnr(pkt[UDP].dport):
                    session['common_protocols'].append('llmnr')
                if parse_udp_mdns(pkt[UDP].dport):
                    session['common_protocols'].append('mdns')
                if parse_tcp_syslog(raw_data):
                    session['common_protocols'].append("syslog")
                if parse_udp_ssdp(raw_data):
                    session['common_protocols'].append("ssdp")
                if parse_udp_bittorrent(raw_data):
                    session['common_protocols'].append("bittorrent")
                if parse_dnp3(raw_data):
                    session['common_protocols'].append("dnp3")
                if parse_udp_radius(raw_data, session['common_spt'], session['common_dpt']):
                    session['common_protocols'].append("radius")
                rpc = parse_udp_rpc(raw_data)
                if rpc is not None:
                    session['common_protocols'].append(rpc)
                if parse_udp_stun(raw_data):
                    session['common_protocols'].append("stun")
                if parse_udp_quic(raw_data):
                    session['common_protocols'].append("quic")
                if parse_udp_bjnp(raw_data):
                    session['common_protocols'].append("bjnp")
                if parse_udp_rip(raw_data, session['common_spt'], session['common_dpt']):
                    session['common_protocols'].append("rip")
                if parse_udp_dhcp(raw_data):
                    session['common_protocols'].append("dhcp")
                if parse_udp_isakmap(raw_data, session['common_dpt']):
                    session['common_protocols'].append("isakmp")
                if parse_udp_memcached(raw_data):
                    session['common_protocols'].append("memcached")
                if parse_udp_safet(pkt[UDP].dport, raw_data):
                    session['common_protocols'].append("safet")
        elif ICMP in pkt:
            session['common_protocols'].append('icmp')
        elif IGMPv3gr in pkt or IGMPv3 in pkt or IGMP in pkt or IGMPv3mr in pkt or IGMPv3mq in pkt or IGMPv3mra in pkt:
            session['common_protocols'].append("igmp")
        else:
            print("没有ip层")
    session['common_protocols'] = list(set(session['common_protocols']))  # 排序
    session['common_protocol_count'] = len(session['common_protocols'])
    session['common_ip_protocol'] = list(set(session['common_ip_protocol']))  # 排序
    print(session)
