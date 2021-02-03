from click import ParamType
from typing import Optional
from ipaddress import IPv6Address, AddressValueError


class IPv6AddressParamType(ParamType):
    name = "ipv6_address"

    @staticmethod
    def validate(ipv6: str) -> Optional[IPv6Address]:
        try:
            return IPv6Address(ipv6)
        except AddressValueError:
            return None

    def convert(self, value, param, ctx):
        ipv6 = self.validate(value)
        if ipv6 is None:
            self.fail("'{0}' is not a valid IPV6 address.".format(value), param, ctx)
        return ipv6


IPV6_ADDRESS = IPv6AddressParamType()
