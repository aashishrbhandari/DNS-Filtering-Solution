class SetupConfigDataHolder:

    def __init__(self,
                dns_server_udp_ip,
                dns_server_udp_port,
                dns_server_tcp_ip,
                dns_server_tcp_port,
                default_auth_dns_server_ip,
                default_auth_dns_server_port,
                dns_server_recv_bytes_size,
                dns_auth_server_recv_bytes_size,
                dns_server_log_debug_on_console,
                category_match_type,
                dns_cache_size,
                dns_cache_ttl
                ):
        self.dns_server_udp_ip = dns_server_udp_ip
        self.dns_server_udp_port = dns_server_udp_port
        self.dns_server_tcp_ip = dns_server_tcp_ip
        self.dns_server_tcp_port = dns_server_tcp_port
        self.default_auth_dns_server_ip = default_auth_dns_server_ip
        self.default_auth_dns_server_port = default_auth_dns_server_port
        self.dns_server_recv_bytes_size = dns_server_recv_bytes_size
        self.dns_auth_server_recv_bytes_size = dns_auth_server_recv_bytes_size
        self.dns_server_log_debug_on_console = self.set_boolean(dns_server_log_debug_on_console);
        self.category_match_type = category_match_type;
        self.dns_cache_size = dns_cache_size;
        self.dns_cache_ttl = dns_cache_ttl;


    def set_boolean(self, boolean_string):
        if  boolean_string.upper() == "TRUE":
            return True
        else:
            return False


    def __repr__(self):
        return f"""
[self.dns_server_udp_ip]: [{self.dns_server_udp_ip}]
[self.dns_server_udp_port]: [{self.dns_server_udp_port}]
[self.dns_server_tcp_ip]: [{self.dns_server_tcp_ip}]
[self.dns_server_tcp_port]: [{self.dns_server_tcp_port}]
[self.default_auth_dns_server_ip]: [{self.default_auth_dns_server_ip}]
[self.default_auth_dns_server_port]: [{self.default_auth_dns_server_port}]
[self.dns_server_recv_bytes_size]: [{self.dns_server_recv_bytes_size}]
[self.dns_auth_server_recv_bytes_size]: [{self.dns_auth_server_recv_bytes_size}]
[self.dns_server_log_debug_on_console]: [{self.dns_server_log_debug_on_console}]
[self.category_match_type]: [{self.category_match_type}]
[self.dns_cache_size]: [{self.dns_cache_size}]
[self.dns_cache_ttl]: [{self.dns_cache_ttl}]
""";