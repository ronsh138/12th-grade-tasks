from scapy.all import IP, ICMP, sr1
import socket
import random
import time

retry = 2
t_o = 0.5


def ping(ttl, host):
    id = 12345
    seq = random.randint(2, 60000)
    pk = (IP(dst=host, ttl=ttl)/ICMP(type = 8, id = id, seq = seq))
    t = time.perf_counter()
    response = sr1(pk, timeout=t_o, verbose=False, retry=retry)
    t2 = time.perf_counter()

    if response is not None:
        print(f"{ttl}. HOST {response.src}, TTL {ttl}, time {(t2-t)*1000:.2f} [ms], Ping Response Type = {response.type}")
        if response.src == host:
            return ttl
    else:
        print(f"{ttl}. .Warning: Host time out, TTL {ttl} Moving on .")
    return 0

if "__main__" == __name__:
    host_ = input("host: ")
    host = socket.gethostbyname(host_)

    count = 1
    ans = ping(count, host)
    while ans == 0:
        count += 1
        ans = ping(count, host)
