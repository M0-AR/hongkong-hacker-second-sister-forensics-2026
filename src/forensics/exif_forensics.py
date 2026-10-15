"""EXIF + GPS forensics — verifies N's karaoke-photo deduction (Ch.4-5).

Claim: photo IMG_6651.jpg carries EXIF DateTimeOriginal 2013-12-24 22:13:55
and GPS pointing to King Wah Centre, Shantung St, Mong Kok. N cross-checks
the date against Kwok-Tai/Lily bringing Siu-Man home Christmas Eve.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExifRecord:
    datetime_original: str  # "YYYY:MM:DD HH:MM:SS"
    gps_lat: float
    gps_lon: float
    make: str = "Apple"
    model: str = "iPhone"


# King Wah Centre approx coords (Mong Kok). Public landmark.
KING_WAH_LAT = 22.3193
KING_WAH_LON = 114.1696


def parse_exif_datetime(s: str) -> datetime:
    return datetime.strptime(s, "%Y:%m:%d %H:%M:%S")


def verify_christmas_eve_link(exif: ExifRecord) -> dict:
    dt = parse_exif_datetime(exif.datetime_original)
    is_christmas_eve = (dt.month, dt.day) == (12, 24) and dt.year == 2013
    # haversine-lite: within ~1km of King Wah Centre?
    dlat = abs(exif.gps_lat - KING_WAH_LAT) * 111.0
    dlon = abs(exif.gps_lon - KING_WAH_LON) * 111.0 * 0.85
    dist_km = (dlat**2 + dlon**2) ** 0.5
    near_king_wah = dist_km < 1.0
    return {
        "datetime": dt.isoformat(),
        "is_2013_christmas_eve": is_christmas_eve,
        "dist_km_to_king_wah": round(dist_km, 3),
        "near_king_wah_centre": near_king_wah,
        "n_inference": (
            "EXIF date matches the ONLY night Kwok-Tai+Lily escorted Siu-Man home; "
            "GPS matches karaoke cluster. Hence photo is contemporaneous, not staged later."
            if (is_christmas_eve and near_king_wah)
            else "No link established."
        ),
    }


def novel_exif_record() -> ExifRecord:
    return ExifRecord(
        datetime_original="2013:12:24 22:13:55",
        gps_lat=22.3193,
        gps_lon=114.1696,
    )
