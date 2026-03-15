#!/usr/bin/env python3
import json

# Load existing findings
with open('known-findings.json', 'r') as f:
    known_data = json.load(f)

# Load new findings
with open('new-findings-2026-03-15.json', 'r') as f:
    new_findings = json.load(f)

# Add new findings to known findings
for finding in new_findings:
    # Create simplified entry for known findings
    known_entry = {
        "id": finding["id"],
        "title": finding["title"],
        "date": finding["date"],
        "category": finding["category"]
    }
    known_data["findings"].append(known_entry)

# Save updated known findings
with open('known-findings.json', 'w') as f:
    json.dump(known_data, f, indent=2, ensure_ascii=False)

print("Updated known-findings.json successfully")