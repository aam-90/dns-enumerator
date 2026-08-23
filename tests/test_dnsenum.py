import dns.resolver
from unittest.mock import patch, MagicMock

from dnsenum.resolver import resolve_records
import json

from dnsenum.output import format_json, format_reverse_json
def test_format_json():
    results = {
        "A": [
            {
                "value": "192.0.2.10",
                "ttl": 300
            }
        ]
    }

    output = format_json("example.com", results)

    data = json.loads(output)

    assert data["target"] == "example.com"
    assert data["records"]["A"][0]["value"] == "192.0.2.10"
    assert data["records"]["A"][0]["ttl"] == 300


def test_format_reverse_json():
    output = format_reverse_json(
        "8.8.8.8",
        ["dns.google."]
    )

    data = json.loads(output)

    assert data["target"] == "8.8.8.8"
    assert data["PTR"] == ["dns.google."]

def test_resolve_a_record_without_real_dns():
    fake_answer = MagicMock()
    fake_answer.rrset.ttl = 300

    fake_record = MagicMock()
    fake_record.to_text.return_value = "192.0.2.10"

    fake_answer.__iter__.return_value = iter([fake_record])

    with patch(
        "dnsenum.resolver.dns.resolver.Resolver.resolve",
        return_value=fake_answer
    ):
        results = resolve_records("example.com", ["A"])

    assert results["A"][0]["value"] == "192.0.2.10"
    assert results["A"][0]["ttl"] == 300


def test_dns_timeout():
    with patch(
        "dnsenum.resolver.dns.resolver.Resolver.resolve",
        side_effect=dns.resolver.Timeout
    ):
        results = resolve_records("example.com", ["A"])

    assert results["A"] == []


from dnsenum.validation import is_valid_domain


def test_valid_domain():
    assert is_valid_domain("example.com") is True


def test_valid_domain_with_trailing_dot():
    assert is_valid_domain("example.com.") is True


def test_invalid_domain():
    assert is_valid_domain("hello!!!") is False


def test_empty_domain():
    assert is_valid_domain("") is False    



