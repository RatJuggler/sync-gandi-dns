from click import ParamType
from ipaddress import ip_address


class IPAddressParamType(ParamType):
    name = "ip_address"

    def convert(self, value, param, ctx):
        try:
            return ip_address(value)
        except TypeError:
            self.fail(
                "expected string for ip_address() conversion, got {0} of type {1}".format(value, type(value).__name__),
                param, ctx)
        except ValueError:
            self.fail("{0} is not a valid IP address".format(value), param, ctx)
