import re

from click import ParamType
from typing import Optional

pattern = re.compile(
    r'^(?:[a-zA-Z0-9]'  # First character of the domain
    r'(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)'  # Sub domain + hostname
    r'+[A-Za-z0-9][A-Za-z0-9-_]{0,61}'  # First 61 characters of the gTLD
    r'[A-Za-z]$'  # Last character of the gTLD
)


class DomainParamType(ParamType):
    name = "domain"

    @staticmethod
    def validate(domain: str) -> Optional[str]:
        try:
            if pattern.match(domain):
                return domain
            else:
                return None
        except TypeError:
            return None

    def convert(self, value, param, ctx):
        domain = self.validate(value)
        if domain is None:
            self.fail("{0} is not a valid domain".format(value), param, ctx)
        return domain


DOMAIN = DomainParamType()
