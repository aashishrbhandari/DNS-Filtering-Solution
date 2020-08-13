import socket

from dnslib import DNSRecord

from base.PolicyHandler import PolicyHandler
from config.ConfigParser import DNS_SERVER_CONFIG_DATA_HOLDER
from config.DnsServerStaticData import DnsServerStaticData
from handlers.CacheHandler import web_category_cache
from handlers.DnsBuilder import DnsBuilder
from handlers.LoggingHandler import logger, timed


class DnsHandler:

    """ Not Implemented """
    def __init__(self):
        pass

    """ If client_Data_holder was added as the instance variable i.e with adding it to self then we do not need to pass it and return it everything saves a lot of complexity [To BE Implemented later]"""

    # Comments Required
    @timed
    def process(self, client_data_holder):
        self.client_data_holder = client_data_holder;
        self.generate_parsed_dns_request();

        self.process_dns_request();
        PolicyHandler.process_policy_check_for_dns_request(client_data_holder=client_data_holder) # Request Filter set the query value to to ALLOW or BLOCK


        if client_data_holder.policy_status.split(":")[0] == "BLOCK":
            self.cache_check(); # Check in Cache [Later change that it also return True or False]
            if client_data_holder.cache_status:
                self.fetch_from_cache() # Get From Cache [It Returns Raw Dns Response]
                return client_data_holder; # now it can be send therefore return it
            else:
                custom_parsed_dns_reponse =  DnsBuilder.create_dns_response(
                    parsed_dns_request=client_data_holder.parsed_dns_request,
                    req_dns_name=client_data_holder.requested_domain,
                    req_dns_type=client_data_holder.requested_query_type) # Create a Block Response
                client_data_holder.parsed_dns_response = custom_parsed_dns_reponse;
                self.dns_response_for_sending()
                return client_data_holder;


        #self.cache_check_and_fetch()
        self.cache_check()

        # Getting the Raw Dns Response [From Cache ] OR [ From Auth Server]
        if self.client_data_holder.cache_status:
            self.fetch_from_cache()
        else:
            self.fetch_from_auth_dns_server()

        if client_data_holder.raw_dns_response:
            self.generate_parsed_dns_response();
        else:
            logger.error(f"[Reason: Cache OR Auth Server Had some Issue and return None "
                         f"-> [{client_data_holder.raw_dns_response}], "
                         f"[Temp Solution: Return Raw Dns Request as Raw Dns Response")
            client_data_holder.raw_dns_response = client_data_holder.raw_dns_request;

        self.process_dns_response();
        PolicyHandler.process_policy_check_for_dns_response(client_data_holder=client_data_holder) # Response Filter

        ## Left To Implement Response Filter if BLOCKED

        if not client_data_holder.cache_status and not client_data_holder.dns_auth_server_timedout:
            logger.debug(f"[Process: Adding Data To Cache], "
                         f"Key: [{client_data_holder.unique_key}], "
                         f"Value: [{client_data_holder.raw_dns_response}], "
                         f"Cache Details: [{web_category_cache.show_cache()}], "
                         f"[Socket TimeOut: [{client_data_holder.dns_auth_server_timedout}]] ");
            web_category_cache.add_to_cache(client_data_holder.unique_key, client_data_holder.raw_dns_response)
        else:
            logger.debug(f"[Process: Don't Add it To Cache], Cache Status: [{client_data_holder.cache_status}] "
                         f"Key: [{client_data_holder.unique_key}], "
                         f"Value: [{client_data_holder.raw_dns_response}], "
                         f"Cache Details: [{web_category_cache.show_cache()}], "
                         f"[Socket TimeOut: [{client_data_holder.dns_auth_server_timedout}]] ");

        self.dns_response_for_sending()
        return client_data_holder


    # Comments Needed
    def generate_parsed_dns_request(self):
        self.client_data_holder.parsed_dns_request = DNSRecord.parse(self.client_data_holder.raw_dns_request);
        logger.debug(f"Parsed Dns Request [RAW] to Dns Object [Dnslib]: \n{self.client_data_holder.parsed_dns_request.toZone()}\n\n");

    # Comments Needed
    def generate_parsed_dns_response(self):
        self.client_data_holder.parsed_dns_response = DNSRecord.parse(self.client_data_holder.raw_dns_response);
        logger.debug(f"Parsed Dns Response [RAW] to Dns Object [Dnslib]: \n{self.client_data_holder.parsed_dns_response.toZone()}\n\n");

    # Comments Required
    def dns_response_for_sending(self):
        self.client_data_holder.parsed_dns_response.header.id = self.client_data_holder.parsed_dns_request.header.id;
        self.client_data_holder.raw_dns_response = DNSRecord.pack(self.client_data_holder.parsed_dns_response)
        logger.debug(f"[Process: Packing Data For Sending], Request_Header_ID: [{self.client_data_holder.parsed_dns_request.header.id}], Response_Data: [{self.client_data_holder.raw_dns_response}]");

    @timed
    def cache_check(self):
        if web_category_cache.check_if_present(self.client_data_holder.unique_key):
            logger.debug(f"[Process: Checking In Cache(FOUND)], Key: [{self.client_data_holder.unique_key}], Value: [NOT SHOWN(Check This)]");
            self.client_data_holder.cache_status = True
        else:
            logger.debug(f"[Process: Checking In Cache(NOT-FOUND)], Key: [{self.client_data_holder.unique_key}], Value: [NOT SHOWN(Check This)]");
            self.client_data_holder.cache_status = False

    # Comments Required
    @timed
    def cache_check_and_fetch(self):
        if web_category_cache.check_if_present(self.client_data_holder.unique_key):
            self.client_data_holder.cache_status = True
            self.client_data_holder = self.fetch_from_cache(self.client_data_holder)
        else:
            self.client_data_holder.cache_status = False
            client_data_holder = self.fetch_from_auth_dns_server(self.client_data_holder)
            return client_data_holder

    # Comments Required
    @timed
    def fetch_from_cache(self):
        raw_dns_response = web_category_cache.get_from_cache(self.client_data_holder.unique_key)
        logger.debug(f"[Process: Fetching From Cache], Key: [{self.client_data_holder.unique_key}], Value: [{raw_dns_response}]");
        self.client_data_holder.raw_dns_response = raw_dns_response;

    # Comments Required
    @timed
    def fetch_from_auth_dns_server(self):
        setup_config_data_holder = DNS_SERVER_CONFIG_DATA_HOLDER.setup_config_data_holder;

        raw_dns_response = None;

        if not self.client_data_holder.auth_server_ip_address:
            from_auth_dns_server = (setup_config_data_holder.default_auth_dns_server_ip, int(setup_config_data_holder.default_auth_dns_server_port));

        dns_auth_server_recv_bytes_size = setup_config_data_holder.dns_auth_server_recv_bytes_size

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2); # Set Time Out To 2 Seconds
            sock.sendto(self.client_data_holder.raw_dns_request, from_auth_dns_server)
            logger.debug(f"[Process: Making UDP Conn to Remote Auth Server], "
                         f"Client Local Socket: [{sock}], "
                         f"Remote Socket: [{from_auth_dns_server}]"
                         f"[Socket Time Out: [{sock.gettimeout()}]]");
            raw_dns_response, server_address = sock.recvfrom(int(dns_auth_server_recv_bytes_size))
        except socket.timeout as socket_timeout:
            logger.debug(f"[Process: Socket TimedOut while fetching dns answer, Reason: [{socket_timeout}]], "
                        f"[Do Not Cache This], [Sending the Same DnsRequest back To Client]"); # Need to Change This
            self.client_data_holder.dns_auth_server_timedout = True
            raw_dns_response = self.client_data_holder.raw_dns_request
        finally:
            sock.close();  ##  Need some changes [CHECK THIS] [Add More Dns if one fails]
            logger.debug(f"[Process: Fetching From Auth Server], Key: [{self.client_data_holder.unique_key}], Value: [{raw_dns_response}]");
            self.client_data_holder.raw_dns_response = raw_dns_response; # set the raw_dns_response

    """ Dns Request handlers """

    # Comments Required
    def process_dns_request(self):
        self.dns_request_extractor();

    # Comments Required
    def get_dns_request_header_details(self, dns_header):
        dns_header_full = dns_header
        dns_header_id = dns_header_full.id;
        return dns_header_full, dns_header_id;

    # The Way the Dns Works, A DnsRequest will only consist of one Question therefore only the first element of the used is processed
    def get_dns_request_question_details(self,):
        dns_question_1 = self.client_data_holder.parsed_dns_request.questions[0];
        dns_question_name = str(dns_question_1.qname);
        dns_question_type = str(dns_question_1.qtype);
        self.client_data_holder.requested_domain = dns_question_name;
        self.client_data_holder.requested_query_type = dns_question_type;
        logger.debug(f"Dns Question Section, Question[0]: [{dns_question_1}] : With Question: [{dns_question_name}] & Type: [{dns_question_type}] ");

    # Comments Required
    def generate_key(self, q_name, q_type):
        key = q_name + "_" + q_type;
        logger.debug(f"[Process: Generating Partial Key Before Policy Results], Unique_Key: [{key}]  ");
        return key;

    # Comments Required
    def dns_request_extractor(self):
        dns_request_header, dns_request_header_id, = self.get_dns_request_header_details(self.client_data_holder.parsed_dns_request.header);
        logger.debug(f"Dns Header Section: of ID: {dns_request_header_id}, Data: [{dns_request_header}]");

        self.client_data_holder.dns_header_id = dns_request_header_id;
        self.get_dns_request_question_details()

        unique_key = self.generate_key(self.client_data_holder.requested_domain, self.client_data_holder.requested_query_type);
        self.client_data_holder.unique_key = unique_key

    """ Dns Response Handlers """

    # Comments Required
    def get_result_list(self, dns_response_rr):
        ip_list = [];
        cname_list = [];
        ptr_list = [];
        for one_dns_response_rr in dns_response_rr:
            if DnsServerStaticData.DNS_QUERY_TYPE.get(one_dns_response_rr.rtype, None) == "A" or DnsServerStaticData.DNS_QUERY_TYPE.get(one_dns_response_rr.rtype, None) == "AAAA":
                ip_list.append(str(one_dns_response_rr.rdata));
            elif DnsServerStaticData.DNS_QUERY_TYPE.get(one_dns_response_rr.rtype, None) == "CNAME":
                cname_list.append(str(one_dns_response_rr.rdata));
            elif DnsServerStaticData.DNS_QUERY_TYPE.get(one_dns_response_rr.rtype, None) == "PTR":
                ptr_list.append(str(one_dns_response_rr.rdata));

        return ip_list, cname_list, ptr_list

    def get_response_details(self, dns_response_rr):
        return self.get_result_list(dns_response_rr);

    # Comments Required: Left To Implement
    def process_dns_response(self):

        ip_list, cname_list, ptr_list = self.get_response_details(self.client_data_holder.parsed_dns_response.rr);
        logger.debug(f"[Process: Getting IP_LIST/CNAME_LIST/PTR_LIST], "
                     f"Type: [{self.client_data_holder.requested_query_type}], "
                     f"Data: [IP(v4/v6):[{ip_list}]], [CNAME:[{cname_list}]], [PTR:[{ptr_list}]]");

        if ip_list:
            self.client_data_holder.response_ip_list = ','.join(ip_list)
        if cname_list:
            self.client_data_holder.response_cname_list = ','.join(cname_list)
        if ptr_list:
            self.client_data_holder.response_ptr_list = ','.join(ptr_list)
