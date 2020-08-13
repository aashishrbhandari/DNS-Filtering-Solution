from dnslib import RR, A, AAAA, QTYPE  # DNS Resource Record (RR)

from handlers.LoggingHandler import logger
from config.DnsServerStaticData import DnsServerStaticData

class DnsBuilder:

    DEFAULT_TTL = 3600;
    DEFAULT_DNS_RESPONSE_ANSWER_IP = "0.0.0.0"

    # Here ip_address_list also can contain domain name or Cname or Ptr record we will change the name later
    @classmethod
    def create_dns_response(cls, parsed_dns_request, req_dns_name, req_dns_type, ip_address_list=["0.0.0.0"]):
        req_dns_type = int(req_dns_type)
        logger.debug(f"[Process Data: [{parsed_dns_request}], [{req_dns_name}], [{req_dns_type}], [{ip_address_list}]]")

        if DnsServerStaticData.DNS_QUERY_TYPE[req_dns_type] == "AAAA":
            ip_address_list = ["::"]

        if not ip_address_list:
            ip_address_list = cls.DEFAULT_DNS_RESPONSE_ANSWER_IP.split();

        logger.debug(f"DnsServerStaticData.DNS_QUERY_TYPE[req_dns_type]: {DnsServerStaticData.DNS_QUERY_TYPE[req_dns_type]}")

        for one_ip_address in ip_address_list:
            if DnsServerStaticData.DNS_QUERY_TYPE[req_dns_type] == "A":
                parsed_dns_request.add_answer(RR(rname=req_dns_name, rtype=QTYPE.A, rdata=A(one_ip_address), ttl=cls.DEFAULT_TTL))
            elif DnsServerStaticData.DNS_QUERY_TYPE[req_dns_type] == "AAAA":
                parsed_dns_request.add_answer(RR(rname=req_dns_name, rtype=QTYPE.AAAA, rdata=AAAA(one_ip_address), ttl=cls.DEFAULT_TTL))
            elif DnsServerStaticData.DNS_QUERY_TYPE[req_dns_type] == "PTR":
                parsed_dns_request.add_answer(*RR.fromZone(f"{req_dns_name} {cls.DEFAULT_TTL} PTR {one_ip_address}"))
            else:
                parsed_dns_request.add_answer(RR(rname=req_dns_name, rtype=QTYPE.A, rdata=A(one_ip_address), ttl=cls.DEFAULT_TTL))
        logger.debug(f"New Dns Response With Answer Added: [{parsed_dns_request}]")
        return parsed_dns_request

    # Will be Implemented later as we will already have a Dns Request Parsed Object (Client Dns Question Object)
    @classmethod
    def create_dns_block_response(cls, req_dns_name, req_dns_type):
        if req_dns_type == "A":
            RR(rname=req_dns_name, rdata=A("1.2.3.4"), ttl=cls.DEFAULT_TTL)
        else:
            RR(rname=req_dns_name, rdata=AAAA("::/0"), ttl=cls.DEFAULT_TTL)



### using dnslib to create Dns Response
"""
    Generate a RR(Resource Record) using class RR
    
    All Fields:
    ------------
    RR(rname="www.google.com", rtype=1, rclass=1, ttl=0, rdata=None)
    
    Usage:
    ------
    
    IPv4 & IPv6 [0.0.0.0]
    RR(rname="abc.com", rdata=A("0.0.0.0"), ttl=900)
    RR(rname="www.google.com", rtype=QTYPE.AAAA, rdata=AAAA("::"), ttl=300)

"""