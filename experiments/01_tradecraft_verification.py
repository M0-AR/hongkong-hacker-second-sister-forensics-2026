"""EXP-01 tradecraft verification — runs N's forensic deductions end-to-end (offline)."""
import json, sys
sys.path.insert(0, "src")
from forensics.ip_forensics import classify_poster, explain_tor_limitation
from forensics.email_forensics import novel_case_report
from forensics.exif_forensics import novel_exif_record, verify_christmas_eve_link
from forensics.wifi_forensics import match_target, mac_random_collision_prob, mitm_library_analogy, stingray_facts

results = {}
results["E1_popcorn_relay"] = classify_poster("212.117.180.21", "X")
results["E1_ordinary"] = classify_poster("1.65.43.119", "Mozilla/5.0 (Linux; U; Android 4.0.4)")
results["E1_tor_note"] = explain_tor_limitation(3)
results["E2_email_headers"] = novel_case_report()
results["E3_exif"] = verify_christmas_eve_link(novel_exif_record())
results["E4_wifi_mac_match"] = {"target": "3E:06:B2:A2:52:F3", "match": match_target("3e:06:b2:a2:52:f3"), "collision_p": mac_random_collision_prob()}
results["E4_mitm"] = mitm_library_analogy()
results["E4_stingray"] = stingray_facts()

# PASS/FAIL gates (verifiable, no hand-waving)
checks = [
    ("relay flagged highly_anonymised", results["E1_popcorn_relay"]["verdict"] == "highly_anonymised_likely_relay"),
    ("ordinary poster distinct", results["E1_ordinary"]["verdict"] == "ordinary_poster"),
    ("3 distinct MTR IPs", results["E2_email_headers"]["n_distinct_ips"] == 3),
    ("iPhone Mail detected", results["E2_email_headers"]["is_iphone"] is True),
    ("EXIF Christmas Eve + King Wah", results["E3_exif"]["is_2013_christmas_eve"] and results["E3_exif"]["near_king_wah_centre"]),
    ("MAC match case-insensitive", results["E4_wifi_mac_match"]["match"] is True),
]
results["checks"] = [{"name": n, "pass": bool(p)} for n, p in checks]
results["overall"] = "PASS" if all(p for _, p in checks) else "FAIL"

with open("results/exp01_tradecraft.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(json.dumps(results, indent=2, ensure_ascii=False))
print("OVERALL:", results["overall"])
assert results["overall"] == "PASS", "EXP-01 failed"
