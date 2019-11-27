from click import ParamType
from ipaddress import IPv6Address, AddressValueError


class IPv6AddressParamType(ParamType):
    name = "ipv6_address"

    def convert(self, value, param, ctx):
        try:
            return IPv6Address(value)
        except AddressValueError:
            self.fail("{0} is not a valid IPV6 address".format(value), param, ctx)
