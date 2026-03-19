#!/usr/bin/env python3

import json

# Read existing findings
with open('known-findings.json', 'r') as f:
    known_data = json.load(f)

# Read new findings
with open('new-findings-2026-03-19.json', 'r') as f:
    new_findings = json.load(f)

# Convert new findings to the known format
for finding in new_findings:
    known_data['findings'].append({
        "id": finding['id'],
        "title": finding['title'],
        "date": "2026-03-19",
        "category": finding['category']
    })

# Write updated known findings
with open('known-findings.json', 'w') as f:
    json.dump(known_data, f, indent=2)

print(f"Added {len(new_findings)} new findings to known-findings.json")