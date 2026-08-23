# DNS Enumerator

A Python-based DNS enumeration and analysis tool built with
[dnspython](https://www.dnspython.org/).

## Features

- Query common DNS record types
- Display record TTL values
- Reverse DNS lookups
- Configurable DNS resolver
- JSON output
- Input validation
- DNS error handling
- Unit tests
- Logging

## What I Learned About DNS

While building this project, I learned how DNS translates human-readable
domain names into information used by networked systems.

### DNS Record Types

- **A** — Maps a domain name to an IPv4 address.
- **AAAA** — Maps a domain name to an IPv6 address.
- **NS** — Identifies the authoritative nameservers for a domain.
- **CNAME** — Creates an alias from one domain name to another.
- **MX** — Specifies mail servers responsible for receiving email.
- **PTR** — Performs reverse DNS mapping from an IP address to a hostname.
- **SOA** — Contains administrative information about a DNS zone.
- **TXT** — Stores text data associated with a domain, commonly used for
  verification and email-related policies.

### TTL

DNS records have a **Time To Live (TTL)** value. It indicates how long a
DNS response may be cached before it should be queried again.

This project displays the TTL for records returned by the resolver.

### Forward and Reverse DNS

A normal lookup is a forward lookup:

```text
domain → IP address

For example:

example.com → 93.184.216.x

A reverse lookup works in the opposite direction:

IP address → hostname

This project supports reverse lookups using PTR records.
DNS Resolvers

A DNS resolver receives DNS queries and obtains answers from DNS servers.

This project normally uses the system-configured resolver, but it can also
use a user-selected DNS server with the --server option.

For example:

python demodns.py example.com --server 8.8.8.8
What This Project Taught Me

Building this project helped me understand:

DNS record types and their purposes
Forward and reverse DNS lookups
DNS TTL and caching
DNS resolver behavior
Handling DNS timeouts and errors
Mocking DNS responses in unit tests
Separating application logic into modules
Command-line argument handling
Structured JSON output
Logging and input validation


## Installation

Clone the repository:

```bash
git clone https://github.com/aam-90/dns-enumerator.git