import json
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'data', 'companies.json')

def validate_data():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format! \n{e}")
        sys.exit(1)

    seen_names = set()
    seen_urls = set()
    has_error = False

    print("🔍 Validating data...")

    for index, company in enumerate(data):
        name = company.get('name', '').strip().lower()
        url = company.get('careers_url', '').strip().lower()

        if name in seen_names:
            print(f"❌ Duplicate Error: Company '{company['name']}' already exists.")
            has_error = True
        else:
            seen_names.add(name)

        if url in seen_urls:
            print(f"❌ Duplicate Error: The URL for '{company['name']}' is already used by another entry.")
            has_error = True
        else:
            seen_urls.add(url)
            
        if company.get('visa_sponsorship') not in ["YES", "NO", "SENIOR_ONLY"]:
            print(f"❌ Value Error: Invalid visa_sponsorship value for '{company['name']}'")
            has_error = True

    if has_error:
        print("\n💥 Validation FAILED. Please fix the errors above.")
        sys.exit(1)
    else:
        print("\n✅ All checks passed! No duplicates found.")
        sys.exit(0)

if __name__ == "__main__":
    validate_data()