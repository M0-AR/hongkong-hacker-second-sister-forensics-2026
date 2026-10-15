import sys
sys.path.insert(0, "src")
from forensics.ip_forensics import classify_poster
from forensics.email_forensics import novel_case_report
from forensics.exif_forensics import novel_exif_record, verify_christmas_eve_link
from forensics.wifi_forensics import match_target

def test_relay_flagged():
    assert classify_poster("212.117.180.21", "X")["verdict"] == "highly_anonymised_likely_relay"

def test_email_headers():
    r = novel_case_report()
    assert r["n_distinct_ips"] == 3 and r["is_iphone"]

def test_exif_link():
    v = verify_christmas_eve_link(novel_exif_record())
    assert v["is_2013_christmas_eve"] and v["near_king_wah_centre"]

def test_mac():
    assert match_target("3E-06-B2-A2-52-F3")
