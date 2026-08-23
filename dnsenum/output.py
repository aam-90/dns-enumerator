import json


def format_json(domain, results):
    return json.dumps(
        {
            "target": domain,
            "records": results
        },
        indent=2
    )
def format_reverse_json(ip_address, results):
    return json.dumps(
        {
            "target": ip_address,
            "PTR": results
        },
        indent=2
    )


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