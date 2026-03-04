#!/usr/bin/env python3

import re
from urllib.parse import urlparse

# Read the current HTML
with open('ai-design-research.html', 'r') as f:
    content = f.read()

def convert_card(match):
    """Convert corrupted card format to original beautiful format"""
    card_content = match.group(0)
    
    # Extract elements from corrupted format
    title_match = re.search(r'<a href="([^"]+)"[^>]*class="finding-title"[^>]*>([^<]+)</a>', card_content)
    source_match = re.search(r'<div class="finding-source"><a href="([^"]+)"[^>]*>([^<]+)</a></div>', card_content)
    desc_match = re.search(r'<p class="finding-desc">([^<]+(?:<[^>]+>[^<]*</[^>]+>)*[^<]*)</p>', card_content, re.DOTALL)
    verdict_match = re.search(r'<p class="finding-verdict"><strong>Verdict:</strong>\s*([^<]+)</p>', card_content)
    tags_match = re.search(r'<div class="finding-tags">(.*?)</div>', card_content, re.DOTALL)
    id_match = re.search(r'id="([^"]+)"', card_content)
    
    if not all([title_match, source_match, desc_match, verdict_match, tags_match]):
        return card_content  # Return unchanged if we can't parse it
    
    url = title_match.group(1)
    title = title_match.group(2)
    description = desc_match.group(1)
    verdict_text = verdict_match.group(1).strip()
    tags_html = tags_match.group(1)
    
    # Generate ID if missing
    card_id = id_match.group(1) if id_match else title.lower().replace(' ', '-').replace('—', '').replace(':', '').replace('(', '').replace(')', '')[:50]
    
    # Clean up URL for source display
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    clean_source = f"{domain}"
    
    # Determine verdict badge based on content
    verdict_class = "watch"  # default
    verdict_display = "Watch"
    if any(word in verdict_text.lower() for word in ['try', 'practical', 'useful', 'worth testing']):
        verdict_class = "try"
        verdict_display = "Try it"
    elif any(word in verdict_text.lower() for word in ['skip', 'avoid', 'not worth']):
        verdict_class = "skip" 
        verdict_display = "Skip"
    elif any(word in verdict_text.lower() for word in ['bookmark', 'save', 'reference']):
        verdict_class = "bookmark"
        verdict_display = "Bookmark"
    
    # Convert tags to proper format
    tags = re.findall(r'<span class="tag[^"]*">([^<]+)</span>', tags_html)
    tags_formatted = ''.join([f'<span class="tag">{tag}</span>' for tag in tags])
    
    # Generate the beautiful card format
    beautiful_card = f'''<div class="finding">
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

# Find and convert all corrupted cards (ones with finding-header and finding-title)
pattern = r'<div class="finding"[^>]*id="[^"]*"[^>]*>.*?<div class="finding-header"><a href="[^"]*"[^>]*class="finding-title".*?</div>\s*</div>'

converted_content = re.sub(pattern, convert_card, content, flags=re.DOTALL)

# Write the converted file
with open('ai-design-research.html', 'w') as f:
    f.write(converted_content)

# Count conversions
original_corrupted = len(re.findall(pattern, content, re.DOTALL))
remaining_corrupted = len(re.findall(pattern, converted_content, re.DOTALL))

print(f"Converted {original_corrupted - remaining_corrupted} cards to beautiful format")
print(f"Remaining corrupted cards: {remaining_corrupted}")