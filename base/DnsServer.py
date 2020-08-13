import logging
import socket
import traceback
from socketserver import DatagramRequestHandler, BaseServer
from threading import Thread, Timer  ## Required for MultiThreaded Server
from time import time as fetch_current_unix_time
from typing import Any

import dnslib
from dnslib import DNSRecord

from config.ConfigParser import DNS_SERVER_CONFIG_DATA_HOLDER
from database.DatabaseHandler import DatabaseHandler
from datastore.ClientDataHolder import ClientDataHolder
from handlers.CacheHandler import web_category_cache
from handlers.DnsBuilder import DnsBuilder
from handlers.DnsHandler import DnsHandler
from handlers.LoggingHandler import timed, logger

"""
Few Details are inside a Class File, they are kept as few things needs to be garbed from a file in order to start 
the initial service and then rest part are taken from the config xml file 
"""

class DnsServer(DatagramRequestHandler):
    """ Default Used From DnsServerConfig File, Also Default We use Google Dns Server """

    """ Initialize the Dns Service with all Important Data like logger, config_xml_data, socket etc ... """
    @timed
    def setup(self) -> None:
        super().setup()
        self.init_config();
        self.DNS_SERVER_UDP_IP = self.setup_config_data_holder.dns_server_udp_ip;
        self.DNS_SERVER_UDP_PORT = self.setup_config_data_holder.dns_server_udp_port;
        self.bind_server_to_socket()  # Bind the Socket

        self.init_database_connection() # Connect to SQLite Database
        self.dns_name_dict(); # Set Dns Name

    def init_database_connection(self):
        self.dns_handler = DatabaseHandler();

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

    """ Get the Important Config Details from the File, which holds all the details  """
    """  Initialize the Logging Service, Static Data is Fetched from DnsServerStaticData """

    @timed
    def init_config(self):
        setup_config_data_holder = DNS_SERVER_CONFIG_DATA_HOLDER.setup_config_data_holder
        self.setup_config_data_holder = setup_config_data_holder;


    """ Setup the Dns Socket and Bind it """

    @timed
    def bind_server_to_socket(self):
        self.DNS_SERVER_UDP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        self.DNS_SERVER_UDP_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.DNS_SERVER_UDP_SOCKET.bind((self.DNS_SERVER_UDP_IP, int(self.DNS_SERVER_UDP_PORT)))

    """ This Method Starts the Dns Service """

    def init_log_uniq_id(self, uniq_id):
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.uniq_id = uniq_id
            return record

        logging.setLogRecordFactory(record_factory)

    @timed
    def start_server(self):
        logger.debug(f"Dns Service Running @ {self.DNS_SERVER_UDP_SOCKET.getsockname()} ");

        while True:
            try:
                dns_request, client_address = self.DNS_SERVER_UDP_SOCKET.recvfrom(1024); ## Received Data from Socket
                #self.validate_and_handle_client(uniq_id, dns_request, client_address); ## Single Threaded
                handler_thread = Thread(target=self.validate_and_handle_client, args=(dns_request, client_address)) ## Making it MultiThreaded
                #handler_thread.setName(f"Dns-Query-Handler-Thread-{uniq_id}")
                logger.debug(f"[Process: Starting Thread: {handler_thread.getName()} with uniq_id: [{uniq_id}]]")
                handler_thread.start(); ## Start The Thread For Processing
            except ConnectionResetError as conn_reset:
                logger.error(f"[Reason: ConnectionResetError]: [ERROR: {conn_reset}]");
            except KeyboardInterrupt as key_cancel:
                logger.error(f"[Reason: KeyboardInterrupt]: [ERROR: {key_cancel}]");
                self.stop_server()
            except Exception as all_exception:
                logger.error(f"[Reason: Exception]: [All Exceptions are handled here][ERROR: {all_exception}]");
                logger.error(traceback.print_exc());
                self.stop_server()




    def validate_and_handle_client(self, dns_request, client_address):
        # Validate & Dns Server Name Setup
        if self.validate_and_dns_name_setup(dns_request=dns_request, client_address=client_address):
            self.handle_client(dns_request, client_address);  ##  Single Threaded

    """ Limitation: No Such Query will be added to database that is forged or incorrect 
        also no query who's dns response is provide by the below function(validate_and_dns_name_setup) provides 
        which is kind of required """
    def validate_and_dns_name_setup(self, dns_request, client_address):
        logger.info(f"[Process : Validate & Dns Name Setup]")  ## Debugging
        validation_result = False
        validation_info = "Improper/Forged Dns Request"
        custom_parsed_dns_response = None
        try:
            parsed_dns_request = DNSRecord.parse(dns_request);
            req_dns_name = str(parsed_dns_request.questions[0].qname);
            req_dns_type = int(parsed_dns_request.questions[0].qtype);
            if req_dns_name in self.dns_name.keys():
                dns_name_to_set = self.dns_name[req_dns_name]
                logger.debug(f"IP ADRR LIST: {dns_name_to_set.split(',')}")
                print(f"IP ADRR LIST: {dns_name_to_set.split(',')}")
                custom_parsed_dns_response = DnsBuilder.create_dns_response(parsed_dns_request=parsed_dns_request,
                                                                             req_dns_name=req_dns_name,
                                                                             req_dns_type=req_dns_type,
                                                                             ip_address_list=dns_name_to_set.split(","));
                validation_info = ""
            else:
                validation_result = True
                validation_info = ""

        except (dnslib.buffer.BufferError, dnslib.dns.DNSError) as dns_parsing_error:
            logger.error(f"[Process: Validation By using parse()] "
                         f"[Error: DnsRecord.parse() Exception, Data Received is INCORRECT, "
                         f"Exception: [{dns_parsing_error}]");
            #logger.error(traceback.pr);
            # Create Response
            '''
            custom_parsed_dns_response = DnsBuilder.create_dns_response(parsed_dns_request=parsed_dns_request,
                                                                        req_dns_name=req_dns_name,
                                                                        req_dns_type=req_dns_type)
            '''
            validation_info = validation_info + f", Exception: [{dns_parsing_error}]"
        except Exception as all_exception:
            logger.error(f"[Process: Validation By using parse()] "
                         f"[Error: Unknown Exception] "
                         f"Exception: [{all_exception}]");
            #logger.error(traceback.print_exc());
            # Create Response
            '''
            custom_parsed_dns_response = DnsBuilder.create_dns_response(parsed_dns_request=parsed_dns_request,
                                                                        req_dns_name=req_dns_name,
                                                                        req_dns_type=req_dns_type)
            '''
            validation_info = validation_info + f", Exception: [{all_exception}]"
        finally:
            #print("custom_parsed_dns_response: ", custom_parsed_dns_response)
            if validation_result:
                logger.debug(f"Process Complete Validation INFO: [{validation_info}, {custom_parsed_dns_response}]")
                return validation_result
            else:
                if validation_info == "":
                    self.send_response_to_client(client_address=client_address, dns_data=DNSRecord.pack(custom_parsed_dns_response), status_tag=validation_info)
                return None


    def handle_client(self, dns_request, client_address):
        logger.debug(f"Dns Request Received from "
                     f"[Client:{client_address}], "
                     f"By [Server:{self.DNS_SERVER_UDP_SOCKET.getsockname()}], "
                     f"[Data:{str(dns_request)}] ");
        client_data_holder = ClientDataHolder(client_ip_address=client_address[0],
                                              client_socket_address=client_address,
                                              raw_dns_request=dns_request);
        client_data_holder.dns_start_time = fetch_current_unix_time()
        dns_handler = DnsHandler()
        client_data_holder = dns_handler.process(client_data_holder=client_data_holder)  # Send it To the Processor
        self.send_response_to_client(client_address, client_data_holder.raw_dns_response,
                                     f"CLIENT-{client_data_holder.policy_status}");
        client_data_holder.dns_end_time = fetch_current_unix_time()
        dns_process_time = (client_data_holder.dns_end_time - client_data_holder.dns_start_time) * 1000;
        logger.debug(f"[Process: Dns Request Handled] took "
                    f"[Raw: {dns_process_time} millis] "
                    f"[Round: {round(dns_process_time, 3)} millis]");
        client_data_holder.dns_process_time = round(dns_process_time, 3)
        logger.debug(client_data_holder);
        self.dns_handler.insert_to_access_db(client_data_holder=client_data_holder); ## Insert Into DB


    """ Send the DnsResponse to the Client """
    @timed
    def send_response_to_client(self, client_address, dns_data, status_tag):
        logger.debug(
            f"[Reason:{status_tag}] Sending Response To [Client:{client_address}], By [Server:{self.DNS_SERVER_UDP_SOCKET.getsockname()}], [Data:{str(dns_data)}] ")
        self.DNS_SERVER_UDP_SOCKET.sendto(dns_data, client_address);

    def handle(self) -> None:
        super().handle()

    def finish(self) -> None:
        super().finish()


    """ Stops the Dns Server """
    @timed
    def stop_server(self):
        logger.error("[Reason: KeyboardInterrupt] Closing/Shutting Dns Service");
        exit();
