from threading import Thread

from base.MultiThreadedDnsServer import MultiThreadedDnsServer
from testing.FileUpdateChecker import start_watchdog

print("""
Dns Server uses the Python File: DnsServerStaticData (Also a class with Same name inside this file)
Please change it before setting it up as it uses Static file path Specific to System [Might Crash the Server if not Proper]
""")

multithreaded_dns_server = MultiThreadedDnsServer() # Create a Server Instance

watch_dog_thread = Thread(target=start_watchdog())
watch_dog_thread.start();

multithreaded_dns_server.start_server() # Start the Server

print("++++++++++++")



multithreaded_dns_server.server_close()
