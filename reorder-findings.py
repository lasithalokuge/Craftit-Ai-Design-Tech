#!/usr/bin/env python3

import re
from datetime import datetime

# Read the current HTML
with open('ai-design-research.html', 'r') as f:
    content = f.read()

# Extract everything before the first day-section
before_sections = content.split('<div class="day-section">')[0]

# Extract everything after the last day-section (footer, etc.)
after_marker = '<!-- ===== RESEARCH ENTRIES GO ABOVE THIS LINE ===== -->'
after_sections = content.split(after_marker)[1] if after_marker in content else content.split('</body>')[0].split('</html>')[0] + '</body>\n</html>'
after_sections = after_marker + after_sections

# Extract all day sections
day_sections = []
pattern = r'<div class="day-section">.*?</div>\s*(?=<div class="day-section">|<!-- ===== RESEARCH ENTRIES GO ABOVE THIS LINE ===== --|</body>)'

for match in re.finditer(pattern, content, re.DOTALL):
    section_content = match.group(0)
    # Extract the date from the h2 tag
    date_match = re.search(r'<h2>(.*?, \d{4})</h2>', section_content)
    if date_match:
        date_str = date_match.group(1)
        try:
            # Parse date like "March 3, 2026"
            date_obj = datetime.strptime(date_str, '%B %d, %Y')
            day_sections.append((date_obj, section_content))
        except:
            print(f"Could not parse date: {date_str}")

print(f"Found {len(day_sections)} day sections")

# Sort by date (newest first)
day_sections.sort(key=lambda x: x[0], reverse=True)

# Rebuild the HTML
new_content = before_sections

for date_obj, section in day_sections:
    new_content += section + '\n\n'

new_content += after_sections

# Write the reordered file
with open('ai-design-research.html', 'w') as f:
    f.write(new_content)

print("Reordered day sections (latest first):")
for date_obj, _ in day_sections:
    print(f"  {date_obj.strftime('%B %d, %Y')}")