from bs4 import BeautifulSoup

from config.DnsServerStaticData import DnsServerStaticData
from datastore.AllowedDataHolder import AllowedDataHolder
from datastore.BlockedDataHolder import BlockedDataHolder
from datastore.ClientDataHolder import ClientDataHolder
from datastore.DnsServerConfigDataHolder import DnsServerConfigDataHolder
from datastore.SetupConfigDataHolder import SetupConfigDataHolder
from handlers.LoggingHandler import logger, timed


class ConfigParser:

    CONFIG_SECTION = ["setup_config", "blocked", "allowed"];

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name;
        self.init_xml_content();
        self.init_bs4_parsed_xml_content();

    def init_xml_content(self):
        with open(self.config_file_name) as xml_config_file:
            self.xml_content = xml_config_file.read();
        logger.debug(f"Processed Data From [File:{self.config_file_name}], XML CONTENT DATA: =>")
        logger.debug(self.xml_content)
        return self.xml_content;

    def init_bs4_parsed_xml_content(self):
        parser_utility = 'html.parser'
        bs4_parsed_xml_content = BeautifulSoup(self.xml_content, parser_utility);
        self.bs4_parsed_xml_content = bs4_parsed_xml_content;
        logger.debug(f"Processed Data From [Parser_Utility:{parser_utility}], [Lib: BeatifulSoup(BS4) Parsed CONTENT DATA: =>")
        logger.debug(self.bs4_parsed_xml_content)
        return self.bs4_parsed_xml_content;

    def process_setup_config_section(self):
        section_content_xml = self.bs4_parsed_xml_content.find_all('setup_config');
        logger.debug(f"Processing [Section:setup_config] Data:")
        logger.debug(section_content_xml)

        dns_server_udp_ip = section_content_xml[0].dns_server_udp_ip.getText().strip();
        dns_server_udp_port = section_content_xml[0].dns_server_udp_port.getText().strip();
        dns_server_tcp_ip = section_content_xml[0].dns_server_tcp_ip.getText().strip();
        dns_server_tcp_port = section_content_xml[0].dns_server_tcp_port.getText().strip();
        default_auth_dns_server_ip = section_content_xml[0].default_auth_dns_server_ip.getText().strip();
        default_auth_dns_server_port = section_content_xml[0].default_auth_dns_server_port.getText().strip();
        dns_server_recv_bytes_size = section_content_xml[0].dns_server_recv_bytes_size.getText().strip();
        dns_auth_server_recv_bytes_size = section_content_xml[0].dns_auth_server_recv_bytes_size.getText().strip();
        dns_server_log_debug_on_console = section_content_xml[0].dns_server_log_debug_on_console.getText().strip();
        dns_cache_size = section_content_xml[0].dns_cache_size.getText().strip();
        dns_cache_ttl = section_content_xml[0].dns_cache_ttl.getText().strip();
        category_match_type = section_content_xml[0].category_match_type.getText().strip();
        return SetupConfigDataHolder(dns_server_udp_ip=dns_server_udp_ip,
                                     dns_server_udp_port=dns_server_udp_port,
                                     dns_server_tcp_ip=dns_server_tcp_ip,
                                     dns_server_tcp_port=dns_server_tcp_port,
                                     default_auth_dns_server_ip=default_auth_dns_server_ip,
                                     default_auth_dns_server_port=default_auth_dns_server_port,
                                     dns_server_recv_bytes_size=dns_server_recv_bytes_size,
                                     dns_auth_server_recv_bytes_size=dns_auth_server_recv_bytes_size,
                                     dns_server_log_debug_on_console=dns_server_log_debug_on_console,
                                     dns_cache_size=dns_cache_size,
                                     dns_cache_ttl=dns_cache_ttl,
                                     category_match_type=category_match_type);

    def process_blocked_section(self):
        blocked = 'blocked';
        section_blocked_xml = self.bs4_parsed_xml_content.find_all(blocked);
        logger.debug(f"Processing [Section: {blocked}] Data:")
        logger.debug(section_blocked_xml)

        block_policy_name = section_blocked_xml[0].block_policy_name.getText().strip();
        block_policy_description = section_blocked_xml[0].block_policy_description.getText().strip();
        block_policy_regex_pattern = section_blocked_xml[0].block_policy_regex_pattern.getText().strip();
        block_policy_webcategory_list = section_blocked_xml[0].block_policy_webcategory_list.getText().strip();

        return BlockedDataHolder(block_policy_name=block_policy_name,
                                 block_policy_description=block_policy_description,
                                 block_policy_regex_pattern=block_policy_regex_pattern,
                                 block_policy_webcategory_list=block_policy_webcategory_list)

    def process_allowed_section(self):
        allowed = 'allowed';
        section_allowed_xml = self.bs4_parsed_xml_content.find_all(allowed);
        logger.debug(f"Processing [Section: {allowed}] Data:")
        logger.debug(section_allowed_xml)

        allow_policy_name = section_allowed_xml[0].allow_policy_name.getText().strip();
        allow_policy_description = section_allowed_xml[0].allow_policy_description.getText().strip();
        allow_policy_regex_pattern = section_allowed_xml[0].allow_policy_regex_pattern.getText().strip();
        allow_policy_webcategory_list = section_allowed_xml[0].allow_policy_webcategory_list.getText().strip();

        return AllowedDataHolder(allow_policy_name=allow_policy_name,
                                 allow_policy_description=allow_policy_description,
                                 allow_policy_regex_pattern=allow_policy_regex_pattern,
                                 allow_policy_webcategory_list=allow_policy_webcategory_list)


def get_dns_server_config_data_holder(config_file=None):
    if config_file:
        logger.debug(f"[IF] Config_File Provided: [{config_file}]")
    else:
        config_file = DnsServerStaticData.DNS_CONFIG_FILE_TEST
        logger.debug(f"[ELSE] Config_File is None, Therefore Set Config_File To: [{config_file}]")

    config_parser = ConfigParser(config_file)
    dns_server_config_data_holder = DnsServerConfigDataHolder()
    for one_config_section in ConfigParser.CONFIG_SECTION:
        if one_config_section == "setup_config":
            logger.debug(f"Processing [Section: {one_config_section}]")
            setup_config_data_holder = config_parser.process_setup_config_section();
            logger.debug("[Holder: SetupConfigDataHolder] Data:");
            logger.debug(setup_config_data_holder);
            dns_server_config_data_holder.setup_config_data_holder = setup_config_data_holder;
        elif one_config_section == "blocked":
            logger.debug(f"Processing [Section: {one_config_section}]")
            blocked_data_holder = config_parser.process_blocked_section();
            logger.debug("[Holder: BlockedDataHolder] Data:");
            logger.debug(blocked_data_holder);
            dns_server_config_data_holder.blocked_data_holder = blocked_data_holder;
        elif one_config_section == "allowed":
            logger.debug(f"Processing [Section: {one_config_section}]")
            allowed_data_holder = config_parser.process_allowed_section();
            logger.debug("[Holder: AllowedDataHolder] Data:");
            logger.debug(allowed_data_holder);
            dns_server_config_data_holder.allowed_data_holder = allowed_data_holder;
        else:
            logger.debug(f"[Reason: Implementation Remaining] NOT Processing [Section: {one_config_section}]")
    return dns_server_config_data_holder



# Process the Block Policy Section Match it with the Client Request and then Return TRUE if Blocked FALSE if NOT
def process_block_policy(client_data_holder, dns_server_config_data_holder,):

    status = { "block_status": True, "block_type": "Regex" }
    #blocked_data_holder: BlockedDataHolder = dns_server_config_data_holder.blocked_data_holder # Good Way for Type Check
    blocked_data_holder = dns_server_config_data_holder.blocked_data_holder

    blocked_regex = blocked_data_holder.block_policy_regex_pattern;
    blocked_webcategory_list = blocked_data_holder.block_policy_webcategory_list.split(',');
    logger.debug(f"block_regex: [{blocked_regex}], block_webcategory_list: [{blocked_webcategory_list}] ")

    # No pattern in BLOCK & No Category Specified, Block ALL, can create problems, But Whitelist [Regex, WebCategory] needs to be Maintained properly then
    if blocked_regex.pattern.strip() == '' and not blocked_webcategory_list:
        status["block_status"] = True
        status["block_type"] = "Regex"
        logger.debug(f"MATCHED[ALL], BLOCK[ALL], Since EMPTY/SPACE, blocked_regex: [{blocked_regex}], Status: [{status}], block_webcategory_list: [{blocked_webcategory_list}] ")
        return status

    if blocked_regex.search(client_data_holder.requested_domain_extracted): # Using Function: search() later changed
        status["block_status"] = True
        status["block_type"] = "Regex"
        logger.debug(f"Matched[BLOCKED:{status}], With RequestDomainExtracted:[{client_data_holder.requested_domain_extracted}]")
    else:
        status["block_status"] = False
        status["block_type"] = "No-Regex-Match"
        logger.debug(f"NOT Matched[BLOCKED:{status}], With RequestDomainExtracted:[{client_data_holder.requested_domain_extracted}]")

        if client_data_holder.web_category_list:
            logger.debug(f"[Process: Checking With Category], Client_WebCategoryList:[{client_data_holder.web_category_list}]")

            if client_data_holder.web_category_list == list:
                webcategory_list = client_data_holder.web_category_list
            else:
                webcategory_list = client_data_holder.web_category_list.split(',')

            if bool(set(webcategory_list).intersection(blocked_webcategory_list)):
                status["block_status"] = True
                status["block_type"] = "WebCategory"
                logger.debug(f"Matched[BLOCKED:{status}]: block_webcategory_list:[{blocked_webcategory_list}] With Client_WebCategoryList:[{webcategory_list}]")
            else:
                logger.debug(f"NOT Matched[BLOCKED:{status}]: block_webcategory_list:[{blocked_webcategory_list}] With Client_WebCategoryList:[{webcategory_list}]")
        else:
            logger.debug(f"[Process: Category Is Empty], Client_WebCategoryList:[{client_data_holder.web_category_list}]")

    return status

def process_allow_policy(client_data_holder, dns_server_config_data_holder):

    status = { "allow_status": True, "allow_type": "Regex" }
    # Process Allowed Section
    #allowed_data_holder: BlockedDataHolder = dns_server_config_data_holder.allowed_data_holder
    allowed_data_holder = dns_server_config_data_holder.allowed_data_holder

    allowed_regex = allowed_data_holder.allow_policy_regex_pattern;
    allowed_webcategory_list = allowed_data_holder.allow_policy_webcategory_list.split(',');
    logger.debug(f"allowed_regex: [{allowed_regex}], allowed_webcategory_list: [{allowed_webcategory_list}] ")

    # No pattern in ALLOW Does not work to allow all
    if allowed_regex.pattern.strip() == '' and not allowed_webcategory_list:
        status["allow_status"] = False
        status["allow_type"] = "Regex"
        logger.debug(f"MATCHED[ALL], BLOCK[ALL], Since EMPTY/SPACE, blocked_regex: [{allowed_regex}], Status: [{status}], block_webcategory_list: [{allowed_webcategory_list}] ")
        return status

    if allowed_regex.search(client_data_holder.requested_domain_extracted):  # Using search later changed
        status["allow_status"] = True
        status["allow_type"] = "Regex"
        logger.debug(f"Matched[ALLOWED:{status}], Regex:[{allowed_regex}] With RequestDomainExtracted:[{client_data_holder.requested_domain_extracted}]")
    else:
        status["allow_status"] = False
        status["allow_type"] = "No-Regex-Match"
        logger.debug(f"NOT Matched[ALLOWED:{status}], Regex:[{allowed_regex}] With RequestDomainExtracted:[{client_data_holder.requested_domain_extracted}]")

        if client_data_holder.web_category_list:
            logger.debug(f"[Process: Checking With Category], Client_WebCategoryList:[{client_data_holder.web_category_list}]")

            if client_data_holder.web_category_list == list:
                webcategory_list = client_data_holder.web_category_list
            else:
                webcategory_list = client_data_holder.web_category_list.split(',')

            if bool(set(webcategory_list).intersection(allowed_webcategory_list)):
                status["allow_status"] = True
                status["allow_type"] = "WebCategory"
                logger.debug(f"Matched[ALLOWED:{status}]: allowed_webcategory_list:[{allowed_webcategory_list}] With Client_WebCategoryList:[{webcategory_list}]")
            else:
                logger.debug(f"NOT Matched[BLOCKED:{status}]: allowed_webcategory_list:[{allowed_webcategory_list}] With Client_WebCategoryList:[{webcategory_list}]")
        else:
            logger.debug(f"[Process: Category Is Empty], Client_WebCategoryList:[{client_data_holder.web_category_list}]")

    return status

@timed
def process_policy(client_data_holder):
    dns_server_config_data_holder = DNS_SERVER_CONFIG_DATA_HOLDER
    #status = { "status": "ALLOW", "type": "Regex" } # Type: Regex or WebCategory
    status = process_block_policy(client_data_holder=client_data_holder, dns_server_config_data_holder=dns_server_config_data_holder)

    # If block True lets's check  Allow Status
    if status.get("block_status"):
        _status = process_allow_policy(client_data_holder=client_data_holder, dns_server_config_data_holder=dns_server_config_data_holder)
        logger.debug(f"Processed Allow Policy Result for Allow:{status}")
        if status.get("allow_status"):
            return { "status": "ALLOW", "type": _status.get("allow_type") }
        else:
            return {"status": "BLOCK", "type": status.get("block_type")}
    else:
        return {"status": "ALLOW", "type": "No-Block-Match"}


DNS_SERVER_CONFIG_DATA_HOLDER = get_dns_server_config_data_holder(config_file=DnsServerStaticData.DNS_CONFIG_FILE_FULL_PATH)

def set_DNS_SERVER_CONFIG_DATA_HOLDER(NEW_DNS_SERVER_CONFIG_DATA_HOLDER):
    global DNS_SERVER_CONFIG_DATA_HOLDER
    DNS_SERVER_CONFIG_DATA_HOLDER = NEW_DNS_SERVER_CONFIG_DATA_HOLDER


if __name__ == "__main__":
    # Testing
    print(f"[File:ConfigParser] [__name__:{__name__}]")
    dns_server_config_data_holder = get_dns_server_config_data_holder(config_file=DnsServerStaticData.DNS_CONFIG_FILE_FULL_PATH)
    print("--------------------------MAIN---------------------------")
    print(dns_server_config_data_holder)
    print("-------------------------Policy Check------------------------")
    client_data_holder = ClientDataHolder(client_ip_address="10.0.1.5", client_socket_address="sadsa", raw_dns_request="sdasda")
    client_data_holder.requested_domain_extracted = "ads.com"
    client_data_holder.web_category_list = "Yahoo"
    status = process_policy(client_data_holder=client_data_holder, dns_server_config_data_holder=dns_server_config_data_holder)
    print(f"Policy Status: [{status}]")

