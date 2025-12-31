from enum import Enum
from datetime import date, datetime
from typing import Dict, Any, List


# =========================
# Enums (Allowed Values)
# =========================

class VisaSponsorship(str, Enum):
    YES = "YES"
    NO = "NO"
    SENIOR_ONLY = "SENIOR_ONLY"


class RemotePolicy(str, Enum):
    GLOBAL = "GLOBAL"
    EU_ONLY = "EU_ONLY"
    HYBRID = "HYBRID"
    ON_SITE = "ON_SITE"


class HiringStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FREEZE = "FREEZE"


# =========================
# Required Fields & Types
# =========================

REQUIRED_FIELDS: Dict[str, type] = {
    "name": str,
    "careers_url": str,
    "locations": list,
    "visa_sponsorship": str,
    "remote_policy": str,
    "tech_stack": list,
    "hiring_status": str,
    "last_updated": str,
}

OPTIONAL_FIELDS: Dict[str, type] = {
    "meta_data": dict,
}


# =========================
# Location Contract
# =========================

LOCATION_REQUIRED_FIELDS: Dict[str, type] = {
    "country": str,
    "city": str,
    "is_hq": bool,
}


# =========================
# Business Rules Helpers
# =========================

def is_valid_date(value: str) -> bool:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
        return parsed <= date.today()
    except ValueError:
        return False


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def has_exactly_one_hq(locations: List[Dict[str, Any]]) -> bool:
    return sum(1 for loc in locations if loc.get("is_hq") is True) == 1
