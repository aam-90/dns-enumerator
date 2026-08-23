import argparse

import socket
import logging
from dnsenum.validation import is_valid_domain, is_valid_nameserver

from dnsenum.resolver import resolve_records, reverse_lookup
from dnsenum.output import (
    print_results,
    format_json,
    format_reverse_json,
)


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


def main():

    logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
    )

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
    parser.add_argument(
    "--server",
    help="DNS server IPv4 or IPv6 address to use for queries"
    )
    
    args = parser.parse_args()

    if args.server and not is_valid_nameserver(args.server):
        print(f"[!] Invalid DNS server address: {args.server}")
        return

    if not args.reverse and not is_valid_domain(args.domain):
        print(f"[!] Invalid domain name: {args.domain}")
        return

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
            print(format_reverse_json(args.domain, results))
        else:
            print(f"\nReverse DNS results for: {args.domain}")
            print("=" * 50)

            if results:
                for hostname in results:
                    print(hostname)
            else:
                print("No PTR record found.")

        return

    results = resolve_records(
    args.domain,
    args.types,
    nameserver=args.server
    )

    if results is None:
        return

    if args.json:
        print(format_json(args.domain, results))
    else:
        print_results(args.domain, results)