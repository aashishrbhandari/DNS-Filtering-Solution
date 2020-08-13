from netaddr import *
from time import time as fetch_current_unix_time
"""
ip_address_list = "192.168.1.0/24,192.168.0.0/24,10.10.10.0/24"

ip = IPNetwork(ip_address_list.split(",")[0])

for one_ip_net in ip_address_list.split(","):
    if "192.168.1.150" in IPNetwork(one_ip_net):
        print("yAy")

"""

ip_addr_str = "192.168.0.0/24,192.168.1.4,192.168.10.1-192.168.10.4"
ip_addr_str_list = ip_addr_str.split(",")

print("ip_addr_str -> ", ip_addr_str)
print("ip_addr_str_list -> ", ip_addr_str_list)

start_time = fetch_current_unix_time()
end_time = fetch_current_unix_time()
dns_process_time = (end_time - start_time) * 1000;
process_time = round(dns_process_time, 3)



check_for_ip = "192.168.10.2"

start_time = fetch_current_unix_time()
for one_ip_group in ip_addr_str_list:
    #print(one_ip_group)
    if "/" in one_ip_group:
        #print("===MATCHES==[/] [Network Segment]", one_ip_group)
        if check_for_ip in IPNetwork(one_ip_group):
            #print(f"MATCHED: {check_for_ip} IN [{one_ip_group}]")
            break;
    elif "-" in one_ip_group:
        #print("===MATCHES==[-] [RANGE]", one_ip_group)
        if check_for_ip in IPRange(one_ip_group.split("-")[0], one_ip_group.split("-")[1]):
            #print(f"MATCHED: {check_for_ip} IN [{one_ip_group}]")
            break;
    else:
        #print("===MATCHES==[DIRECT IP]", one_ip_group)
        if check_for_ip == one_ip_group:
            #print(f"MATCHED: {check_for_ip} IN [{one_ip_group}]")
            break;

end_time = fetch_current_unix_time()
dns_process_time = (end_time - start_time) * 1000;
process_time = round(dns_process_time, 3)
print("process_time -> ", process_time)