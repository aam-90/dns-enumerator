import dns.resolver
import dns.reversename
import logging


logger = logging.getLogger(__name__)

def resolve_records(domain, record_types, nameserver=None):
    results = {}

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 5

    if nameserver:
       resolver.nameservers = [nameserver]


    for record_type in record_types:
        try:
            answer = resolver.resolve(domain, record_type)

            records = []

            for record in answer:
                records.append({
                    "value": record.to_text(),
                    "ttl": answer.rrset.ttl
                })

            results[record_type] = records

        except dns.resolver.NoAnswer:
            results[record_type] = []

        except dns.resolver.NXDOMAIN:
            print(f"[!] Domain does not exist: {domain}")
            return None

        except dns.resolver.NoNameservers:
            results[record_type] = []
            logger.warning("No nameservers available for %s", record_type)

        except dns.resolver.Timeout:
            results[record_type] = []
            logger.warning("DNS timeout while querying %s", record_type)

        except dns.exception.DNSException as error:
            results[record_type] = []
            logger.error("DNS error for %s: %s", record_type, error)

    return results


def reverse_lookup(ip_address):
    try:
        reverse_name = dns.reversename.from_address(ip_address)
        answer = dns.resolver.resolve(reverse_name, "PTR")

        return [record.to_text() for record in answer]

    except dns.resolver.NXDOMAIN:
        return []

    except dns.resolver.NoAnswer:
        return []

    except dns.resolver.Timeout:
        logger.warning("Reverse DNS lookup timed out.")
        return []

    except dns.exception.DNSException as error:
        print(f"[!] Reverse DNS error: {error}")
        return []