import time
from pprint import pprint

from cachetools import TTLCache

cache = TTLCache(maxsize=10, ttl=3)

cache['apple1'] = 'top dog'
cache['apple2'] = 'top dog'
cache['apple3'] = 'top dog'
cache['apple4'] = 'top dog'
cache['apple5'] = 'top dog'
cache['apple6'] = 'top dog'
cache['apple7'] = 'top dog'
cache['apple8'] = 'top dog'
cache['apple9'] = 'top dog'
cache['apple10'] = 'top dog'

pprint(cache)

print("Sleeping for 2 Seconds")
time.sleep(2)

print("Fetching the data again to check if get will preserver log fro more time")
print(cache.get('apple2'))
pprint(cache)

cache["mango1"] = "mango 2"

print("Sleeping for 2 Seconds")
time.sleep(2)
print("After 2 Seconds")
pprint(cache)