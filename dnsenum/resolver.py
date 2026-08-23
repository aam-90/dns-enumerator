import logging

import dns.exception
import dns.resolver
import dns.reversename


logger = logging.getLogger(__name__)


def resolve_records(domain, record_types, nameserver=None):
    results = {}

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 5

    # Use a custom DNS server if one was provided
    if nameserver:
        resolver.nameservers = [nameserver]
        logger.info("Using custom DNS server: %s", nameserver)

    logger.info("Starting DNS lookup for %s", domain)

    for record_type in record_types:
        logger.info(
            "Querying %s record for %s",
            record_type,
            domain
        )

        try:
            answer = resolver.resolve(domain, record_type)

            records = []

            for record in answer:
                records.append(
                    {
                        "value": record.to_text(),
                        "ttl": answer.rrset.ttl,
                    }
                )

            results[record_type] = records

            logger.info(
                "Found %d %s record(s) for %s",
                len(records),
                record_type,
                domain,
            )

        except dns.resolver.NoAnswer:
            results[record_type] = []
            logger.info(
                "No %s records found for %s",
                record_type,
                domain,
            )

        except dns.resolver.NXDOMAIN:
            logger.error(
                "Domain does not exist: %s",
                domain
            )
            return None

        except dns.resolver.NoNameservers:
            results[record_type] = []

            logger.warning(
                "No nameservers available for %s",
                record_type
            )

        except dns.resolver.Timeout:
            results[record_type] = []

            logger.warning(
                "DNS timeout while querying %s",
                record_type
            )

        except dns.exception.DNSException as error:
            results[record_type] = []

            logger.error(
                "DNS error for %s: %s",
                record_type,
                error
            )

    return results


def reverse_lookup(ip_address):
    logger.info(
        "Starting reverse DNS lookup for %s",
        ip_address
    )

    try:
        reverse_name = dns.reversename.from_address(ip_address)

        answer = dns.resolver.resolve(
            reverse_name,
            "PTR"
        )

        results = [
            record.to_text()
            for record in answer
        ]

        logger.info(
            "Found %d PTR record(s) for %s",
            len(results),
            ip_address,
        )

        return results

    except dns.resolver.NXDOMAIN:
        logger.info(
            "No reverse DNS domain found for %s",
            ip_address
        )
        return []

    except dns.resolver.NoAnswer:
        logger.info(
            "No PTR record found for %s",
            ip_address
        )
        return []

    except dns.resolver.Timeout:
        logger.warning(
            "Reverse DNS lookup timed out for %s",
            ip_address
        )
        return []

    except dns.exception.DNSException as error:
        logger.error(
            "Reverse DNS error for %s: %s",
            ip_address,
            error
        )
        return []