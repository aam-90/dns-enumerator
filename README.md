# DNS Enumerator

A Python-based DNS enumeration and analysis tool built with `dnspython`.

The tool performs DNS record lookups, reverse DNS lookups, displays TTL
information, supports custom DNS resolvers, and can output results in JSON
format.

> **Note:** This project was built for learning, system administration, and
> authorized security testing.

---

## Features

- Query common DNS record types
- Display DNS record TTL values
- Perform reverse DNS lookups
- Use a custom DNS resolver
- Output results as structured JSON
- Validate domain and IP address input
- Handle DNS errors and timeouts
- Structured logging with verbose output
- Unit tests using `pytest`
- Mock DNS responses during testing
- GitHub Actions CI for automated tests

---

## Supported DNS Record Types

| Record Type | Description |
|---|---|
| `A` | Maps a domain name to an IPv4 address |
| `AAAA` | Maps a domain name to an IPv6 address |
| `NS` | Identifies authoritative nameservers |
| `CNAME` | Creates an alias from one domain name to another |
| `MX` | Specifies mail servers for a domain |
| `PTR` | Maps an IP address to a hostname |
| `SOA` | Contains administrative information about a DNS zone |
| `TXT` | Stores text data such as verification and email policies |

---

# What I Learned About DNS

## DNS Resolution

DNS translates human-readable domain names into information used by
networked systems.

For example:

```text
example.com
    ↓
DNS Resolver
    ↓
DNS Servers
    ↓
93.184.216.x

A DNS resolver receives a query and obtains DNS information from the
appropriate DNS servers.

By default, this project uses the system-configured DNS resolver. A custom
DNS server can also be specified with the --server option.

TTL

DNS records have a Time To Live (TTL) value.

TTL indicates how long a DNS response may be cached before it should
normally be queried again.

For example:   93.184.216.34  (TTL: 300)
This project displays the TTL for DNS records returned by the resolver.

Forward and Reverse DNS

Forward Lookup
A normal DNS lookup is a forward lookup: Domain Name → IP Address

Reverse Lookup
A reverse DNS lookup works in the opposite direction:IP Address → Hostname

This project performs reverse DNS lookups using PTR records.

What This Project Taught Me

Building this project helped me learn about:

DNS record types and their purposes
Forward and reverse DNS lookups
DNS TTL and caching
DNS resolver behavior
DNS timeouts and error handling
Python exception handling
Mocking DNS responses in unit tests
Writing tests with pytest
Separating application logic into modules
Command-line argument handling with argparse
Structured JSON output
Logging in Python
Input validation
Git and GitHub workflows
Continuous integration with GitHub Actions

Project Structure:
dns-enumerator/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── dnsenum/
│   ├── __init__.py
│   ├── resolver.py
│   ├── output.py
│   └── validation.py
│
├── tests/
│   └── test_dnsenum.py
│
├── demodns.py
├── requirements.txt
├── README.md
└── .gitignore

## Installation

Clone the repository:

```bash
git clone https://github.com/aam-90/dns-enumerator.git