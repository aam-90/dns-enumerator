import re
import ipaddress

DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[A-Za-z0-9]"
    r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
)


def is_valid_domain(domain):
    if not isinstance(domain, str):
        return False

    domain = domain.strip().rstrip(".")

    if not domain:
        return False

    return DOMAIN_PATTERN.fullmatch(domain) is not None

def is_valid_nameserver(nameserver):
    try:
        ipaddress.ip_address(nameserver)
        return True
    except ValueError:
        return False    