import multiprocessing

from xbase_util.common_util import build_es_expression, s2date, process_origin_pos
from xbase_util.es_db_util import EsDb
from xbase_util.esreq import EsReq
from xbase_util.pcap_util import process_session_id_disk_simple

if __name__ == '__main__':
    # session_id = '250114-TsLfaA3I48ZPoLAEcvHvUnmr'
    session_id = '250114-Is6JV5wlcN1Fu4M1BLpd0hEu'
    es_exp = build_es_expression(1, f"id=={session_id}", s2date("2025-01-14 18:46:00"), s2date("2025/01/14 18:46:14"),
                                 bounded_type='last')
    # req = EsReq("http://10.28.1.140:9200")
    req = EsReq("http://10.211.55.5:9201")
    res = req.search(es_exp).json()['hits']['hits'][0]
    session = res['_source']
    node = session['node']
    esdb = EsDb(req, multiprocessing.Manager())
    packetPos = session['packetPos']
    stream, packet_list = process_session_id_disk_simple(session_id,
                                                         session['node'],
                                                         process_origin_pos(session['packetPos']),
                                                         esdb,
                                                         "/Users/jimo/Downloads/raw/")
    print(packet_list)
    print(len(stream))
