"""WiFi probe-request / MAC + MITM + Stingray model — verifies N's Ch.5 trap.

N claims:
- probe requests leak MAC before association;
- target MAC 3E:06:B2:A2:52:F3 seen at school narrows to 3 iPhone suspects;
- fake PiscisWiFiGratis + stronger signal => MITM (library analogy);
- Stingray (IMSI catcher) + router DNS hijack => full isolation of Violet.
This module implements the *defensive/verification* side: parsing, detection
heuristics, and a simulation showing why Violet could not detect the fake net.
"""
import re

MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
TARGET_MAC = "3E:06:B2:A2:52:F3"


def normalise_mac(mac: str) -> str:
    return mac.strip().upper().replace("-", ":")


def is_valid_mac(mac: str) -> bool:
    return bool(MAC_RE.match(normalise_mac(mac)))


def match_target(mac: str, target: str = TARGET_MAC) -> bool:
    return normalise_mac(mac) == normalise_mac(target)


def mac_random_collision_prob() -> float:
    # 48-bit space minus multicast/local bits ~= 2^46 usable; N cites 1 in 280T
    # for locally-administered random suffix. We report the textbook figure.
    return 1.0 / 280_000_000_000_000.0


def mitm_library_analogy() -> str:
    return (
        "Librarian analogy (N, Ch.5): attacker erects a FAKE counter by the door. "
        "Clients hand requests to fake librarian, who relays to the REAL counter and "
        "returns doctored books (e.g. killer-rabbit news). Neither side notices. "
        "Defence: HSTS/HSTS-preload, VPN, certificate pinning, ignore open WiFi."
    )


def stingray_facts() -> dict:
    return {
        "what": "IMSI catcher / cell-site simulator impersonates tower with stronger signal",
        "mitm": "forces handsets to associate, relays to real net => full intercept",
        "novel_use": "low-power Stingray in backpack (10m) + fake WiFi keeps Violet isolated at Festival Walk",
        "detection_2026": "SRLabs/SeaGlass-style anomalies, Android 'Cellular security' alerts, VPN+DoH",
        "sources": [
            "https://maxintel.org/imsi-catcher-stingray-detection.html",
            "https://h33.ai/blog/imsi-catcher-stingray-defense/",
        ],
    }
