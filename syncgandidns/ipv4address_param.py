from typing import Optional

from click import ParamType
from ipaddress import IPv4Address, AddressValueError


class IPv4AddressParamType(ParamType):
    name = "ipv4_address"

    @staticmethod
    def validate(ipv4: str) -> Optional[IPv4Address]:
        try:
            return IPv4Address(ipv4)
        except AddressValueError:
            return None

    def convert(self, value, param, ctx):
        ipv4 = self.validate(value)
        if ipv4 is None:
            self.fail("{0} is not a valid IPV4 address".format(value), param, ctx)
        return ipv4
