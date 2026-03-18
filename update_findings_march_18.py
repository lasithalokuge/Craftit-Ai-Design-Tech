#!/usr/bin/env python3

import json

# Read existing known findings
with open('known-findings.json', 'r') as f:
    known_findings = json.load(f)

# Read today's new findings
with open('new-findings-2026-03-18.json', 'r') as f:
    new_findings = json.load(f)

# Convert new findings to known findings format
for finding in new_findings:
    # Determine category based on verdict
    category = "tool"
    if finding["verdict"] == "Try it":
        category = "tool"
    elif finding["verdict"] == "Watch it":
        category = "update"
    
    known_finding = {
        "id": finding["id"],
        "title": finding["title"],
        "date": finding["date"],
        "category": category
    }
    
    # Check if already exists
    exists = any(kf["id"] == finding["id"] for kf in known_findings["findings"])
    
    if not exists:
        known_findings["findings"].append(known_finding)
        print(f"Added: {finding['title']}")
    else:
        print(f"Skipped (duplicate): {finding['title']}")

# Write back to file
with open('known-findings.json', 'w') as f:
    json.dump(known_findings, f, indent=2)

print(f"Total findings now: {len(known_findings['findings'])}")