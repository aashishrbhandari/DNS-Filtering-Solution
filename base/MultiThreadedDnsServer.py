from socketserver import ThreadingUDPServer
from threading import Thread

from config.ConfigParser import DNS_SERVER_CONFIG_DATA_HOLDER
from handlers.DnsRequestHandler import DnsRequestHandler
from handlers.LoggingHandler import logger
from testing.FileUpdateChecker import start_watchdog

setup_config_data_holder = DNS_SERVER_CONFIG_DATA_HOLDER.setup_config_data_holder

# ThreadingUDPServer => ThreadingUDPServer(ThreadingMixIn, UDPServer)
class MultiThreadedDnsServer(ThreadingUDPServer):

    def __init__(self):
        self.DNS_SERVER_UDP_IP = setup_config_data_holder.dns_server_udp_ip; # Server IP
        self.DNS_SERVER_UDP_PORT = setup_config_data_holder.dns_server_udp_port; # Server Port
        self.DNS_SERVER_UDP_SOCKET = (self.DNS_SERVER_UDP_IP, int(self.DNS_SERVER_UDP_PORT))
        super().__init__(server_address=self.DNS_SERVER_UDP_SOCKET, RequestHandlerClass=DnsRequestHandler, bind_and_activate=True)

    def start_server(self):
        logger.debug(f"[Process: Starting Dns Server @ [{self.server_address}]");
        print(f"[Process: Starting Dns Server @ [{self.server_address}]");
        reason = None;
        try:
            self.serve_forever(); #Start The Server
        except ConnectionResetError as conn_reset:
            logger.error(f"[Reason: ConnectionResetError]: [ERROR: {conn_reset}]", exc_info=True); # Stack Trace the Exception
            reason = conn_reset;
        except KeyboardInterrupt as key_cancel:
            logger.error(f"[Reason: KeyboardInterrupt]: [ERROR: {key_cancel}]", exc_info=True); # Stack Trace the Exception
            reason = key_cancel;
        except Exception as all_exception:
            logger.error(f"[Reason: Exception]: [All Exceptions are handled here][ERROR: {all_exception}]", exc_info=True); # Stack Trace the Exception
            reason = all_exception;
        finally:
            self.stop_server(reason=reason)

    def stop_server(self, reason):
        logger.error(f"[Reason: {reason}] Closing/Shutting Dns Service");
        self.server_close()
        exit();



''' Start Dns Server
multithreaded_dns_server = MultiThreadedDnsServer() # Create a Server Instance
multithreaded_dns_server.start_server() # Start the Server
multithreaded_dns_server.server_close()
'''