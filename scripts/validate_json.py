import json
import sys
import os
from typing import Any, Dict, List
from collections import defaultdict

from schema import (
    REQUIRED_FIELDS,
    OPTIONAL_FIELDS,
    LOCATION_REQUIRED_FIELDS,
    VisaSponsorship,
    RemotePolicy,
    HiringStatus,
    is_valid_date,
    is_non_empty_string,
    has_exactly_one_hq,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "data", "companies.json")


# =========================
# Load JSON
# =========================

def load_json() -> List[Dict[str, Any]]:
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format:\n{e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("❌ Root JSON must be a list of companies")
        sys.exit(1)

    return data


# =========================
# Company Validation
# =========================

def validate_company(company: Dict[str, Any], index: int) -> Dict[str, List[str]]:
    errors: Dict[str, List[str]] = defaultdict(list)

    # Required fields
    for field, field_type in REQUIRED_FIELDS.items():
        if field not in company:
            errors["Required Fields"].append(
                f"Missing required field '{field}'"
            )
        elif not isinstance(company[field], field_type):
            errors["Required Fields"].append(
                f"Field '{field}' must be of type {field_type.__name__}"
            )

    # Optional fields
    for field, field_type in OPTIONAL_FIELDS.items():
        if field in company and not isinstance(company[field], field_type):
            errors["Optional Fields"].append(
                f"Optional field '{field}' must be of type {field_type.__name__}"
            )

    # Name
    if "name" in company and not is_non_empty_string(company["name"]):
        errors["Field Errors"].append(
            "Field 'name' cannot be empty"
        )

    # Careers URL
    if "careers_url" in company:
        url = company["careers_url"]
        if not is_non_empty_string(url):
            errors["Field Errors"].append(
                "Field 'careers_url' cannot be empty"
            )
        elif not url.startswith("http"):
            errors["Field Errors"].append(
                f'careers_url="{url}" → must start with http or https'
            )

    # Enum validations
    if "visa_sponsorship" in company:
        value = company["visa_sponsorship"]
        if value not in VisaSponsorship._value2member_map_:
            errors["Enum Errors"].append(
                f'visa_sponsorship="{value}" → use one of: '
                + ", ".join(VisaSponsorship._value2member_map_.keys())
            )

    if "remote_policy" in company:
        value = company["remote_policy"]
        if value not in RemotePolicy._value2member_map_:
            errors["Enum Errors"].append(
                f'remote_policy="{value}" → use one of: '
                + ", ".join(RemotePolicy._value2member_map_.keys())
            )

    if "hiring_status" in company:
        value = company["hiring_status"]
        if value not in HiringStatus._value2member_map_:
            errors["Enum Errors"].append(
                f'hiring_status="{value}" → use one of: '
                + ", ".join(HiringStatus._value2member_map_.keys())
            )

    # Locations
    locations = company.get("locations")
    if not isinstance(locations, list) or not locations:
        errors["Location Errors"].append(
            "locations must be a non-empty list"
        )
    else:
        for i, loc in enumerate(locations):
            if not isinstance(loc, dict):
                errors["Location Errors"].append(
                    f"locations[{i}] must be an object"
                )
                continue

            for field, field_type in LOCATION_REQUIRED_FIELDS.items():
                if field not in loc:
                    errors["Location Errors"].append(
                        f"locations[{i}] missing field '{field}'"
                    )
                elif not isinstance(loc[field], field_type):
                    errors["Location Errors"].append(
                        f"locations[{i}].{field} must be of type {field_type.__name__}"
                    )

        if not has_exactly_one_hq(locations):
            errors["Location Errors"].append(
                "There must be exactly ONE HQ location (is_hq: true)"
            )

    # Tech stack
    tech = company.get("tech_stack")
    if not isinstance(tech, list) or not tech:
        errors["Field Errors"].append(
            "tech_stack must be a non-empty list"
        )

    # Date
    if "last_updated" in company:
        value = company["last_updated"]
        if not is_valid_date(value):
            errors["Date Errors"].append(
                f'last_updated="{value}" → must be YYYY-MM-DD and not in the future'
            )

    return errors


# =========================
# Validate All Companies
# =========================

def validate_all() -> bool:
    companies = load_json()
    has_errors = False

    seen_names = set()
    seen_urls = set()

    print("🔍 Validating companies.json...\n")

    for idx, company in enumerate(companies):
        company_name = company.get("name", f"index {idx}")
        errors = validate_company(company, idx)

        # Duplicate checks
        name_key = str(company.get("name", "")).strip().lower()
        url_key = str(company.get("careers_url", "")).strip().lower()

        if name_key:
            if name_key in seen_names:
                errors["Duplicate Errors"].append("Duplicate company name")
            seen_names.add(name_key)

        if url_key:
            if url_key in seen_urls:
                errors["Duplicate Errors"].append("Duplicate careers_url")
            seen_urls.add(url_key)

        if errors:
            has_errors = True
            print(f"❌ Company [{idx}] — {company_name}")
            for section, messages in errors.items():
                print(f"  🔴 {section}")
                for msg in messages:
                    print(f"   - {msg}")
            print()

    return not has_errors


# =========================
# CLI Entry Point
# =========================

def main() -> None:
    if not validate_all():
        print("💥 Validation FAILED.")
        sys.exit(1)

    print("✅ Validation PASSED. All companies are valid.")


if __name__ == "__main__":
    main()
