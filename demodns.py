import argparse
import json
import socket
import dns.resolver
import dns.reversename


DEFAULT_RECORD_TYPES = [
    "A",
    "AAAA",
    "NS",
    "CNAME",
    "MX",
    "PTR",
    "SOA",
    "TXT",
]


def resolve_records(domain, record_types):
    results = {}

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 5

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
            print(f"[!] No nameservers available for {record_type}")

        except dns.resolver.Timeout:
            results[record_type] = []
            print(f"[!] DNS timeout while querying {record_type}")

        except dns.exception.DNSException as error:
            results[record_type] = []
            print(f"[!] DNS error for {record_type}: {error}")

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
        print("[!] Reverse DNS lookup timed out.")
        return []

    except dns.exception.DNSException as error:
        print(f"[!] Reverse DNS error: {error}")
        return []


def print_results(domain, results):
    print(f"\nDNS results for: {domain}")
    print("=" * 50)

    for record_type, records in results.items():
        print(f"\n{record_type} Records")
        print("-" * 30)

        if not records:
            print("No records found.")
            continue

        for record in records:
            print(f"{record['value']}  (TTL: {record['ttl']})")


def main():
    parser = argparse.ArgumentParser(
        description="Basic DNS enumeration and analysis tool"
    )

    parser.add_argument(
        "domain",
        help="Domain name to query"
    )

    parser.add_argument(
        "-t",
        "--types",
        nargs="+",
        choices=DEFAULT_RECORD_TYPES,
        default=DEFAULT_RECORD_TYPES,
        help="DNS record types to query"
    )

    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Perform a reverse DNS lookup when the target is an IP address"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print results as JSON"
    )

    args = parser.parse_args()

    if args.reverse:
        try:
            socket.inet_pton(socket.AF_INET, args.domain)
        except OSError:
            try:
                socket.inet_pton(socket.AF_INET6, args.domain)
            except OSError:
                print("[!] --reverse requires a valid IPv4 or IPv6 address.")
                return

        results = reverse_lookup(args.domain)

        if args.json:
            print(json.dumps({
                "target": args.domain,
                "PTR": results
            }, indent=2))
        else:
            print(f"\nReverse DNS results for: {args.domain}")
            print("=" * 50)

            if results:
                for hostname in results:
                    print(hostname)
            else:
                print("No PTR record found.")

        return

    results = resolve_records(args.domain, args.types)

    if results is None:
        return

    if args.json:
        print(json.dumps({
            "target": args.domain,
            "records": results
        }, indent=2))
    else:
        print_results(args.domain, results)


if __name__ == "__main__":
    main()