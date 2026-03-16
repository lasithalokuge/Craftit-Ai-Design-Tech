#!/usr/bin/env python3
"""Fix collapsible structure for all day sections."""

import re

# Read the HTML file
with open('ai-design-research.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern to match day-section divs that don't already have day-content
pattern = r'(<div class="day-section">\s*<div class="day-header">.*?</div>)\s*((?:(?!<div class="day-section">|<div class="day-content">).)*?)(?=<div class="day-section">|</div>\s*</body>|$)'

def wrap_content(match):
    header = match.group(1)
    content = match.group(2).strip()
    
    if not content:
        return header
    
    # Skip if already has day-content
    if 'day-content' in content:
        return match.group(0)
    
    return f"{header}\n\n<div class=\"day-content\">\n{content}\n</div>\n"

# Apply the transformation
fixed_html = re.sub(pattern, wrap_content, html, flags=re.DOTALL)

# Write back
with open('ai-design-research-fixed.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print("✅ Fixed collapsible structure for all sections")