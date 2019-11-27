from click import ParamType
from ipaddress import IPv4Address, AddressValueError


class IPv4AddressParamType(ParamType):
    name = "ipv4_address"

    def convert(self, value, param, ctx):
        try:
            return IPv4Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV4 address".format(value), param, ctx)
