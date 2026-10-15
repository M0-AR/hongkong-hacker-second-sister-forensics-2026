"""Email-header forensics — verifies N's Gmail Received + X-Mailer deduction (Ch.4)."""
import re
from typing import List, Dict

RECEIVED_RE = re.compile(
    r"Received:\s*from\s*\[[^\]]+\]\s*\((?P<host>[^)]+)\s*\[(?P<ip>[\d.]+)\]\)",
    re.IGNORECASE,
)
XMAILER_RE = re.compile(r"X-Mailer:\s*(?P<mailer>.+)", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def parse_received_headers(raw: str) -> List[Dict[str, str]]:
    out = []
    for m in RECEIVED_RE.finditer(raw):
        out.append({"host": m.group("host").strip(), "ip": m.group("ip").strip()})
    return out


def parse_x_mailer(raw: str) -> str | None:
    m = XMAILER_RE.search(raw)
    return m.group("mailer").strip() if m else None


def is_iphone_mailer(xmailer: str | None) -> bool:
    return bool(xmailer and "iPhone Mail" in xmailer)


def hongkong_provider_hint(host: str) -> bool:
    return "netvigator" in host.lower()


NOVEL_HEADERS = """Received: from [10.167.128.165] (1-65-43-119.static.netvigator.com [1.65.43.119])
\\tBy smtp.gmail.com with ESMTPSA id u31sm8172637pfa.81.2015.05.05.01.57.23
Received: from [10.191.138.91] (tswc3199.netvigator.com [218.102.4.199])
\\tBy smtp.gmail.com with ESMTPSA id 361sm8262529pfc.63.2015.05.05.02.04.19
Received: from [10.191.140.110] (1-65-67-221.static.netvigator.com [1.65.67.221])
\\tBy smtp.gmail.com with ESMTPSA id 11sm5888169pfk.91.2015.05.05.02.06.33
X-Mailer: iPhone Mail (11D257)"""


def novel_case_report() -> dict:
    recvd = parse_received_headers(NOVEL_HEADERS)
    ips = [r["ip"] for r in recvd]
    mailer = parse_x_mailer(NOVEL_HEADERS)
    return {
        "n_received": len(recvd),
        "distinct_ips": sorted(set(ips)),
        "n_distinct_ips": len(set(ips)),
        "x_mailer": mailer,
        "is_iphone": is_iphone_mailer(mailer),
        "all_hk_netvigator": all(hongkong_provider_hint(r["host"]) for r in recvd),
        "n_inference": (
            "3 distinct HK Netvigator IPs in ~9 min + iPhone Mail 11D257 (iOS 7.1.2) "
            "=> sender moving between MTR station WiFis (Yau Ma Tei/Mong Kok/Prince Edward), "
            "not a multi-hop proxy chain (all local). Narrows suspect pool to iPhone owners."
        ),
    }
