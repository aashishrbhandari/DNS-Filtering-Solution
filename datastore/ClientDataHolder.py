class ClientDataHolder:

    def __init__(self, client_ip_address, client_socket_address, raw_dns_request):
        self.client_ip_address = client_ip_address
        self.client_socket_address = client_socket_address
        self.client_mac_address = None
        self.auth_server_ip_address = None
        self.auth_server_socket = None
        self.requested_domain = None
        self.requested_domain_extracted = None
        self.requested_query_type = None
        self.policy_status = None
        self.unique_key = None
        self.web_category_list = None
        self.response_ip_list = None
        self.response_cname_list = None
        self.response_ptr_list = None
        self.cache_status = None
        self.web_category_cache_status = None
        self.client_applicable_data_holder = None
        self.dns_auth_server_timedout = False
        self.raw_dns_request = raw_dns_request
        self.parsed_dns_request = None
        self.raw_dns_response = None
        self.parsed_dns_response = None
        self.dns_header_id = None
        self.dns_start_time = None
        self.dns_end_time = None
        self.dns_process_time = None


    """ Left to Implement Getter & Setter """


    def __repr__(self):
        return f"""[client_data_holder] -> 
[client_ip_address]: [{self.client_ip_address}],
[client_socket_address]: [{self.client_socket_address}], 
[client_mac_address]: [{self.client_mac_address}], 
[auth_server_ip_address]: [{self.auth_server_ip_address}],
[auth_server_socket]: [{self.auth_server_socket}],
[requested_domain]: [{self.requested_domain}],
[requested_domain_extracted]: [{self.requested_domain_extracted}],
[requested_query_type]: [{self.requested_query_type}],
[policy_status]: [{self.policy_status}],
[unique_key]: [{self.unique_key}],
[web_category_list]: [{self.web_category_list}],
[response_ip_list]: [{self.response_ip_list}],
[response_cname_list]: [{self.response_cname_list}],
[response_ptr_list ]: [{self.response_ptr_list }],
[cache_status]: [{self.cache_status}],
[web_category_cache_status]: [{self.web_category_cache_status}],
[client_applicable_data_holder]: [{self.client_applicable_data_holder}],
[dns_auth_server_timedout]: [{self.dns_auth_server_timedout}],
[raw_dns_request]: \n[{self.raw_dns_request}],
[parsed_dns_request]: \n[{self.parsed_dns_request}],
[raw_dns_response]: \n[{self.raw_dns_response}],
[parsed_dns_response]: \n[{self.parsed_dns_response}],
[dns_header_id]: [{self.dns_header_id}]
[dns_start_time]: [{self.dns_start_time}]
[dns_end_time]: [{self.dns_end_time}]
[dns_process_time]: [{self.dns_process_time}]

""";


