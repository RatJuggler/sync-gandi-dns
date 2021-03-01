import re

from click import ParamType
from typing import Optional

pattern = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)+[A-Z0-9][A-Z0-9-_]{0,61}[A-Z]|'  # see domain validation
    r'localhost|'  # or localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip address
    r'(?::\d+)?$',  # optional port
    re.IGNORECASE
)


class UrlParamType(ParamType):
    name = "url"

    @staticmethod
    def validate(url: str) -> Optional[str]:
        try:
            if pattern.match(url):
                return url
            else:
                return None
        except TypeError:
            return None

    def convert(self, value, param, ctx):
        url = self.validate(value)
        if url is None:
            self.fail("'{0}' is not a valid URL.".format(value), param, ctx)
        return url


URL = UrlParamType()
