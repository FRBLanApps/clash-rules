import json
import sys
from pathlib import Path

def normalize_domain(url):
    url = url.strip()
    if not url:
        return None
    if url.startswith("*."):
        url = url[2:]
    return f"+.{url}"

json_data = json.load(sys.stdin)
ms_domains = []
ms_cidrs = []
instant_domains = []
instant_cidrs = []
for item in json_data:
    target_domains = instant_domains if item.get("serviceArea") == "Skype" else ms_domains
    target_cidrs = instant_cidrs if item.get("serviceArea") == "Skype" else ms_cidrs
    for url in item.get("urls", []):
        domain = normalize_domain(url)
        if domain:
            target_domains.append(domain)
    for cidr in item.get("ips", []):
        cidr = cidr.strip()
        if cidr:
            target_cidrs.append(cidr)

Path("ms-365.txt").write_text("payload:\n" + "\n".join(f"  - '{d}'" for d in ms_domains) + ("\n" if ms_domains else ""), encoding="utf-8")
Path("ms-365-instant.txt").write_text("payload:\n" + "\n".join(f"  - '{d}'" for d in instant_domains) + ("\n" if instant_domains else ""), encoding="utf-8")
Path("ms-365cidr.txt").write_text("payload:\n" + "\n".join(f"  - '{c}'" for c in ms_cidrs) + ("\n" if ms_cidrs else ""), encoding="utf-8")
Path("ms-365-instantcidr.txt").write_text("payload:\n" + "\n".join(f"  - '{c}'" for c in instant_cidrs) + ("\n" if instant_cidrs else ""), encoding="utf-8")