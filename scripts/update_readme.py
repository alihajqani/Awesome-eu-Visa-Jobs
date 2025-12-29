import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'data', 'companies.json')
README_PATH = os.path.join(BASE_DIR, 'README.md')

def load_data():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(companies):
    md_content = """# 🇪🇺 Europe Tech Visa Jobs

A curated list of European tech companies offering **Visa Sponsorship** and **Remote Work**.

**[🌐 Visit the Website (Search & Filter)](https://alihajqani.github.io/Awesome-eu-Visa-Jobs)**

## 🚀 Company List
| Company | Locations | Visa Sponsorship | Remote Policy | Tech Stack |
|:---|:---|:---:|:---:|:---|
"""
    
    for company in companies:
        name_link = f"[{company['name']}]({company['careers_url']})"
        
        locs = "<br>".join([f"{l['city']}, {l['country']}" for l in company['locations']])
        
        visa_icon = "✅" if company['visa_sponsorship'] == "YES" else "⚠️ Senior" if company['visa_sponsorship'] == "SENIOR_ONLY" else "❌"
        
        remote_map = {
            "GLOBAL": "🌎 Global",
            "EU_ONLY": "🇪🇺 EU Only",
            "HYBRID": "🏢 Hybrid",
            "ON_SITE": "📍 On-Site"
        }
        remote_icon = remote_map.get(company['remote_policy'], company['remote_policy'])
        
        tech = ", ".join(company.get('tech_stack', [])[:3])
        
        row = f"| {name_link} | {locs} | {visa_icon} | {remote_icon} | {tech} |\n"
        md_content += row

    md_content += """
## 🤝 How to Contribute
1. Fork this repository.
2. Edit `data/companies.json`.
3. Add your company details (follow the existing format).
4. Submit a Pull Request!
"""
    return md_content

def update_readme():
    try:
        companies = load_data()
        companies.sort(key=lambda x: x['name'])
        
        new_content = generate_markdown(companies)
        
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("✅ README.md successfully updated!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_readme()