
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




## Installation

Clone the repository:

```bash
git clone https://github.com/aam-90/dns-enumerator.git