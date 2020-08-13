import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent
from time import time as fetch_current_unix_time

from config.ConfigParser import get_dns_server_config_data_holder, set_DNS_SERVER_CONFIG_DATA_HOLDER
from config.DnsServerStaticData import DnsServerStaticData

""" Article Explaining it: https://stackoverflow.com/questions/21587415/python-watchdog-modified-and-created-duplicate-events/21589102#21589102 """
class MyHandler(PatternMatchingEventHandler):

    patterns=["*.xml"]
    counter = 1;

    def on_modified(self, event):
        if type(event) == FileModifiedEvent:
            print("FileModifiedEvent")
            if self.counter == 1:
                print(f"Counter: [{self.counter}] [File is Flushed, IF Read is Performed NO Data can be Read], [Process: Don't Read the File]")
                self.counter = self.counter + 1;
            elif self.counter == 2:
                print(f"Counter: [{self.counter}] [File is Closed, Perform Read Data can be Read Now], [Process: Read the File]")
                print("Process XMl CONFIG")
                NEW_1 = get_dns_server_config_data_holder(config_file=event.src_path)
                set_DNS_SERVER_CONFIG_DATA_HOLDER(NEW_1)
                self.counter = 1 # Set Counter Back to 1


def start_watchdog():
    print("Starting WatchDog Server Monitoring for Config File")
    observer = Observer()
    observer.schedule(MyHandler(), path=DnsServerStaticData.DNS_CONFIG_FULL_PATH)
    observer.start()
    print("End of Function start_watchdog")

if __name__ == '__main__':
    start_watchdog()
