"""IP / Tor / relay forensics — verifies N's claims Ch.2-3."""
import ipaddress
import re

# Known Tor exit / relay example from novel: 212.117.180.21 (Luxembourg)
NOVEL_RELAY_IP = "212.117.180.21"

# Minimal illustrative Tor relay list (publicly documented ranges, truncated).
# In production this is refreshed from Tor bulk exit list / Dan.me.uk.
ILLUSTRATIVE_TOR_SET = {
    "212.117.180.21",
    "185.220.100.240",
    "185.220.101.4",
}

IPV4_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def is_valid_ipv4(ip: str) -> bool:
    try:
        return isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address)
    except ValueError:
        return False


def is_single_char_user_agent(ua: str) -> bool:
    """Novel signal: Kidkit727 User-Agent was literally 'X' (hand-crafted)."""
    return ua.strip() == "X"


def classify_poster(ip: str, user_agent: str, tor_set=None) -> dict:
    """Reproduce N's decision rule: relay + anonymised UA => high anonymisation."""
    tor_set = tor_set or ILLUSTRATIVE_TOR_SET
    valid = is_valid_ipv4(ip)
    on_tor = ip in tor_set
    masked_ua = is_single_char_user_agent(user_agent)
    # anonymisation score: 0..2
    score = int(on_tor) + int(masked_ua)
    verdict = (
        "highly_anonymised_likely_relay"
        if score >= 1 and valid
        else "invalid_ip" if not valid else "ordinary_poster"
    )
    return {
        "ip": ip,
        "valid_ipv4": valid,
        "on_known_relay": on_tor,
        "masked_user_agent": masked_ua,
        "anonymisation_score": score,
        "verdict": verdict,
    }


def explain_tor_limitation(n_relays: int) -> str:
    return (
        f"With {n_relays} chained relays, tracing requires logs from EVERY hop. "
        "If any single relay keeps no recoverable logs, the chain dies — "
        "'like looking for a needle at the bottom of the ocean' (N, Ch.2)."
    )
