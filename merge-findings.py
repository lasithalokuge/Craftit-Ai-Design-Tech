#!/usr/bin/env python3

import re

# Read the current beautiful template (only has up to Feb 26)
with open('ai-design-research.html', 'r') as f:
    current = f.read()

# Read the full version with all findings (up to March 3)
with open('full-march3.html', 'r') as f:
    full = f.read()

# Find the insertion point in current file
insertion_point = current.find('<!-- ===== RESEARCH ENTRIES GO ABOVE THIS LINE ===== -->')
if insertion_point == -1:
    insertion_point = current.find('</body>')

# Extract the missing day sections from full version
# Find all day sections from Feb 27 onwards
pattern = r'<div class="day-section">.*?<div class="day-header">.*?<h2>(February 2[789], 2026|March [123], 2026)</h2>.*?</div>\s*(?=<div class="day-section">|<!-- ===== RESEARCH ENTRIES GO ABOVE THIS LINE ===== --|</body>)'

missing_sections = []
for match in re.finditer(pattern, full, re.DOTALL):
    missing_sections.append(match.group(0))

print(f"Found {len(missing_sections)} missing day sections")

# Insert the missing sections before the insertion point
if missing_sections:
    before = current[:insertion_point]
    after = current[insertion_point:]
    
    # Add the missing sections
    new_content = before
    for section in reversed(missing_sections):  # Reverse to get chronological order
        new_content += section + '\n\n'
    new_content += after
    
    # Update the stats in the header
    total_findings = len(re.findall(r'<div class="finding"', new_content))
    new_content = re.sub(r'(<div class="stat">)\d+', f'\\g<1>{total_findings}', new_content)
    
    # Write the merged file
    with open('ai-design-research.html', 'w') as f:
        f.write(new_content)
    
    print(f"Restored {len(missing_sections)} day sections with {total_findings} total findings")
else:
    print("No missing sections found")