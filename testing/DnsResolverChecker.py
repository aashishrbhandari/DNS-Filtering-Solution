"""
import dns.reversename
name_addr = dns.name.Name(b"252.0.0.224.in-addr.arpa.")
print(name_addr)

asd =  dns.reversename.to_address(name=name_addr)
print(asd)
"""

from dns import reversename
from dns.name import Name


domain_address = reversename.from_address('8.8.4.4')
print(domain_address)
print(type(domain_address))


#domain_address_1 = Name("4.4.8.8.in-addr.arpa.")
domain_address_1 = Name("4.4.8.8")
domain_address_2 = Name('8.8.8.8')

print(" domain_address_1 -> " ,domain_address_1)
print(" domain_address_1 -> ", type(domain_address_1))

print(" domain_address_2 -> " ,domain_address_2)
print(" domain_address_2 -> ", type(domain_address_2))


#print domain_address
#4.4.8.8.in-addr.arpa.

ip_address = reversename.to_address(domain_address_1)
print( "Reverse to normal: ", ip_address)
#8.8.4.4