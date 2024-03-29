import re

from click import ParamType
from typing import Optional

pattern = re.compile(
    r'^(?:[A-Z0-9]'  # First character of the domain
    r'(?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)'  # Sub domain + hostname
    r'+[A-Z0-9][A-Z0-9-_]{0,61}'  # First 61 characters of the gTLD
    r'[A-Z]$',  # Last character of the gTLD
    re.IGNORECASE
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
            self.fail("'{0}' is not a valid domain.".format(value), param, ctx)
        return domain

    def split_envvar_value(self, rv):
        return rv.split(';')


DOMAIN = DomainParamType()
