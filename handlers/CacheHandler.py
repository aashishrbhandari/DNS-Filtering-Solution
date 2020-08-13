""" Quick Normal Implementation for Python Dict In-Memory Cache [Not Effective]"""
from cachetools import TTLCache

from config.ConfigParser import DNS_SERVER_CONFIG_DATA_HOLDER
from handlers.LoggingHandler import logger

setup_config_data_holder = DNS_SERVER_CONFIG_DATA_HOLDER.setup_config_data_holder

class DefaultCacheHandler:

    def __init__(self):
        self.cache = {}

    def add_to_cache(self, key, value):
        self.cache[key] = value
        return self.cache

    def get_from_cache(self, key):
        return self.cache.get(key)

    def check_if_present(self, required_key):
        if required_key in self.cache.keys():
            return True
        else:
            return False

    def show_cache(self):
        return self.cache


class InMemoryCacheHandler:

    def __init__(self):
        dns_cache_size = int(setup_config_data_holder.dns_cache_size)
        dns_cache_ttl = int(setup_config_data_holder.dns_cache_ttl)
        self.cache = TTLCache(maxsize=dns_cache_size, ttl=dns_cache_ttl)

    def add_to_cache(self, key, value):
        self.cache[key] = value
        return self.cache

    def get_from_cache(self, key):
        return self.cache.get(key)

    def check_if_present(self, required_key):
        if required_key in self.cache.keys():
            return True
        else:
            return False

    def show_cache(self):
        logger.debug(f"[Process: Show Cache], "
                     f"CurrentCacheSize: [{self.cache.currsize}], "
                     f"[MaxCacheSize: {self.cache.maxsize}], "
                     f"[CacheTTL: {self.cache.ttl}], "
                     f"[CacheTimer: {self.cache.timer}]")

    def clear_cache(self):
        logger.debug(f"[Process: Clearing Cache], "
                     f"CurrentCacheSize: [{self.cache.currsize}], "
                     f"[MaxCacheSize: {self.cache.maxsize}], "
                     f"[CacheTTL: {self.cache.ttl}], "
                     f"[CacheTimer: {self.cache.timer}]")
        self.cache.clear();


def init_web_category_cache():
    """ Left to Implement Cache """
    implemented = True;

    if implemented:
        return InMemoryCacheHandler()
    else:
        return DefaultCacheHandler()


web_category_cache = init_web_category_cache()
