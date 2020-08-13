from socketserver import DatagramRequestHandler

import dnslib
from dns import name as dns_name
from dns import reversename as dns_reversename
from dnslib import DNSRecord
from time import time as fetch_current_unix_time
from getmac import get_mac_address

from config.DnsServerStaticData import DnsServerStaticData
from database.DatabaseHandler import AccessDatabaseHandler
from datastore.ClientDataHolder import ClientDataHolder
from handlers.DnsBuilder import DnsBuilder
from handlers.DnsHandler import DnsHandler
from handlers.LoggingHandler import logger, timed


class BaseDnsRequestHandler(DatagramRequestHandler):

    def dns_name_dict(self):
        set_all = False
        if set_all:
            self.dns_name = {
                "1.0.0.127.in-addr.arpa.": "DnsFilterv3",  # Add More later
                "3.0.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.0.f.f.ip6.arpa.": "DnsFilterv3",
                "2.0.0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.0.f.f.ip6.arpa.": "DnsFilterv3",
                "252.0.0.224.in-addr.arpa.": "DnsFilterv3",
                "0.0.0.0.in-addr.arpa.": "DnsFilterv3"
            }
        else:
            self.dns_name = {
                "1.0.0.127.in-addr.arpa.": "DnsFilterv3"
            }
        current_dns_name = self.name_to_ptr(self.DNS_SERVER_UDP_IP);
        self.dns_name[current_dns_name] = "DnsFilterv3";

    def name_to_ptr(self, name):
        name_into_list = name.split('.');
        name_into_list.reverse();
        return '.'.join(name_into_list) + '.in-addr.arpa.'

    def validate_and_handle_client(self, dns_request, client_address):
        if self.validate_and_dns_name_setup(dns_request=dns_request, client_address=client_address): # Validate & Dns Server Name Setup
            self.handle_client(dns_request, client_address);

    """ Limitation: No Such Query will be added to database that is forged or incorrect 
        also no query who's dns response is provide by the below function(validate_and_dns_name_setup) provides 
        which is kind of required 
    """
    def validate_and_dns_name_setup(self, dns_request, client_address):
        logger.debug(f"[Process : Validate & Dns Name Setup]")  ## Debugging
        validation_result = False
        validation_info = "Improper/Forged Dns Request"
        custom_parsed_dns_response = None
        try:
            parsed_dns_request = DNSRecord.parse(dns_request);
            req_dns_name = str(parsed_dns_request.questions[0].qname);
            req_dns_type = int(parsed_dns_request.questions[0].qtype);
            if req_dns_name in self.dns_name.keys():
                dns_name_to_set = self.dns_name[req_dns_name]
                logger.debug(f"IP ADDR LIST: {dns_name_to_set.split(',')}")
                custom_parsed_dns_response = DnsBuilder.create_dns_response(parsed_dns_request=parsed_dns_request,
                                                                             req_dns_name=req_dns_name,
                                                                             req_dns_type=req_dns_type,
                                                                             ip_address_list=dns_name_to_set.split(","));
                validation_info = ""
            else:
                validation_result = True
                validation_info = ""
                self.domain_name_extractor(requested_domain_name=req_dns_name, requested_domain_name_type=req_dns_type) #Extract Proper Info From the Dns Requested Domain

        except (dnslib.buffer.BufferError, dnslib.dns.DNSError) as dns_parsing_error:
            logger.error(f"[Process: Validation By using parse()] "
                         f"[Error: DnsRecord.parse() Exception, Data Received is INCORRECT, "
                         f"Exception: [{dns_parsing_error}]", exc_info=True); # Enable StackTrace in Logs
            validation_info = validation_info + f", Exception: [{dns_parsing_error}]"
        except Exception as all_exception:
            logger.error(f"[Process: Validation By using parse()] "
                         f"[Error: Unknown Exception] "
                         f"Exception: [{all_exception}]", exc_info=True); # Enable StackTrace in Logs
            validation_info = validation_info + f", Exception: [{all_exception}]"
        finally:
            if validation_result:
                logger.debug(f"Process Complete Validation INFO: [{validation_info}, {custom_parsed_dns_response}]")
                return validation_result
            else:
                if validation_info == "":
                    self.send_response_to_client(client_address=client_address, raw_dns_response=DNSRecord.pack(custom_parsed_dns_response), status_tag=validation_info)
                return None


    def handle_client(self, dns_request, client_address):
        logger.debug(f"Dns Request Received from "
                     f"[Client:{client_address}], "
                     f"By [Server:{self.DNS_SERVER_UDP_SOCKET}], "
                     f"[Data:{str(dns_request)}] ");
        self.client_data_holder = ClientDataHolder(client_ip_address=client_address[0],
                                              client_socket_address=client_address,
                                              raw_dns_request=dns_request);
        #self.client_data_holder.client_mac_address = self.get_mac(client_ip=client_address[0]) # Added to Get the Actual name of the query [Very Slow Function Do Not Use]
        self.client_data_holder.requested_domain_extracted = self.domain_name_extracted # Added to Get the Actual name of the query

        self.client_data_holder.dns_start_time = fetch_current_unix_time()
        self.client_data_holder = DnsHandler().process(client_data_holder=self.client_data_holder)  # Send it To the Processor
        self.send_response_to_client(client_address,
                                     self.client_data_holder.raw_dns_response,
                                     f"CLIENT-{self.client_data_holder.policy_status}"
                                     );
        self.client_data_holder.dns_end_time = fetch_current_unix_time()
        dns_process_time = (self.client_data_holder.dns_end_time - self.client_data_holder.dns_start_time) * 1000;

        logger.debug(f"[Process: Dns Request Handled] took "
                    f"[Raw: {dns_process_time} millis] "
                    f"[Round: {round(dns_process_time, 3)} millis]");
        self.client_data_holder.dns_process_time = round(dns_process_time, 3)

        logger.debug(self.client_data_holder);

    @timed
    def get_mac(self, client_ip):
        return get_mac_address(ip=client_ip)

    def domain_name_extractor(self, requested_domain_name, requested_domain_name_type):
        if DnsServerStaticData.DNS_QUERY_TYPE.get(requested_domain_name_type, None) == "PTR" :
            dns_name_Name = dns_name.from_text(requested_domain_name) # Convert into dns.name[Name]
            actual_domain_name = dns_reversename.to_address(dns_name_Name);
            self.domain_name_extracted = actual_domain_name;
        else:
            self.domain_name_extracted = requested_domain_name[:-1]

    def send_response_to_client(self, client_address, raw_dns_response, status_tag):
        logger.debug(
            f"[Reason:{status_tag}] Sending Response To [Client:{client_address}], "
            f"By [Server:{self.DNS_SERVER_UDP_SOCKET}], "
            f"[Data:{str(raw_dns_response)}]")
        self.wfile.write(raw_dns_response) # Write Data To Client But is only Flushed when Finish is called


class DnsRequestHandler(BaseDnsRequestHandler):

    # Step 0(Entry Point): server as be used to access server details
    def __init__(self, request, client_address, server):
        self.DNS_SERVER_UDP_IP = server.DNS_SERVER_UDP_IP;
        self.DNS_SERVER_UDP_PORT = server.DNS_SERVER_UDP_PORT;
        self.DNS_SERVER_UDP_SOCKET = server.DNS_SERVER_UDP_SOCKET;
        super().__init__(request, client_address, server)

    # Step 1
    def setup(self):
        super().setup()
        self.dns_name_dict();  # Set Dns Name

    # Step 2
    def handle(self):
        raw_dns_request = self.rfile.read(1024) # Read From Client Read
        self.validate_and_handle_client(dns_request=raw_dns_request, client_address=self.client_address)

    # Step 3: Does the Flush
    def finish(self):
        super().finish()  # Flush the Data to Client & Then Write To Database [Currently Sqlite is Used]
        try:
            database_handler = AccessDatabaseHandler();
            with database_handler.get_connection() as db_connection:  # Db Context Way to Insert and Commit Quickly
                AccessDatabaseHandler.insert_to_access_db(db_connection=db_connection,
                                                    client_data_holder=self.client_data_holder);  ## Insert Into DB
                ## Commit [Currently each insert is committed we we actually later on change it to 1000 Transaction and then commit it]
            database_handler.close_db_connection();

        except AttributeError as client_data_holder_not_present:
            logger.error(f"[Reason: AttributeError], Details: [{client_data_holder_not_present}]")
        except Exception as all_exception:
            print(f"[EXCEPTION: {all_exception}], client_Data_holder to insert: ", self.client_data_holder)
            logger.error(f"[EXCEPTION: {all_exception}], client_Data_holder to insert: {self.client_data_holder}")


