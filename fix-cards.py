#!/usr/bin/env python3

import re
from urllib.parse import urlparse

# Read the current HTML
with open('ai-design-research.html', 'r') as f:
    content = f.read()

def extract_domain_date(url):
    """Extract clean domain from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    return domain

def determine_verdict(verdict_text):
    """Determine verdict badge from text"""
    text_lower = verdict_text.lower()
    if any(word in text_lower for word in ['try', 'practical', 'useful', 'worth testing', 'use']):
        return ('try', 'Try it')
    elif any(word in text_lower for word in ['skip', 'avoid', 'not worth']):
        return ('skip', 'Skip')  
    elif any(word in text_lower for word in ['bookmark', 'save', 'reference']):
        return ('bookmark', 'Bookmark')
    else:
        return ('watch', 'Watch')

def fix_card(match):
    """Convert corrupted card to beautiful format"""
    card_content = match.group(0)
    
    # Extract the card ID from the opening div
    id_match = re.search(r'<div class="finding"[^>]*id="([^"]*)"', card_content)
    card_id = id_match.group(1) if id_match else 'unknown-id'
    
    # Extract title and URL
    title_match = re.search(r'<a href="([^"]*)"[^>]*class="finding-title"[^>]*>([^<]*)</a>', card_content)
    if not title_match:
        return card_content
    
    url = title_match.group(1)
    title = title_match.group(2)
    
    # Extract description
    desc_match = re.search(r'<p class="finding-desc">([^<]*(?:<[^>]*>[^<]*</[^>]*>)*[^<]*)</p>', card_content, re.DOTALL)
    if not desc_match:
        return card_content
    description = desc_match.group(1).strip()
    
    # Extract verdict
    verdict_match = re.search(r'<p class="finding-verdict"><strong>Verdict:</strong>\s*([^<]*)</p>', card_content)
    if not verdict_match:
        return card_content
    verdict_text = verdict_match.group(1).strip()
    verdict_class, verdict_display = determine_verdict(verdict_text)
    
    # Extract tags
    tags_match = re.search(r'<div class="finding-tags">(.*?)</div>', card_content, re.DOTALL)
    if not tags_match:
        return card_content
    
    tags_html = tags_match.group(1)
    tags = re.findall(r'<span class="tag[^"]*">([^<]*)</span>', tags_html)
    
    # Generate clean source
    clean_source = extract_domain_date(url)
    
    # Build the beautiful card
    tags_formatted = '\n            '.join([f'<span class="tag">{tag}</span>' for tag in tags])
    
    beautiful_card = f'''      <div class="finding">
        <div class="finding-header">
          <h4><a href="{url}" target="_blank" id="{card_id}">{title}</a></h4>
          <span class="verdict {verdict_class}">{verdict_display}</span>
        </div>
        <div class="source-url"><a href="{url}" target="_blank">{clean_source}</a></div>
        <p class="desc">{description}</p>
        <div class="finding-footer">
          <div class="tags">
            {tags_formatted}
          </div>
        </div>
      </div>'''
    
    return beautiful_card

# Pattern to match corrupted cards
corrupted_pattern = r'<div class="finding"[^>]*id="[^"]*"[^>]*>\s*<div class="finding-header"><a href="[^"]*"[^>]*class="finding-title".*?</div>\s*</div>'

# Count before
original_count = len(re.findall(corrupted_pattern, content, re.DOTALL))

# Fix all corrupted cards
fixed_content = re.sub(corrupted_pattern, fix_card, content, flags=re.DOTALL)

# Count after  
remaining_count = len(re.findall(corrupted_pattern, fixed_content, re.DOTALL))

# Write the fixed content
with open('ai-design-research.html', 'w') as f:
    f.write(fixed_content)

print(f"Fixed {original_count - remaining_count} corrupted cards")
print(f"Remaining corrupted cards: {remaining_count}")

if remaining_count > 0:
    print("\nFirst remaining corrupted card:")
    remaining = re.findall(corrupted_pattern, fixed_content, re.DOTALL)
    if remaining:
        print(remaining[0][:200] + "...")