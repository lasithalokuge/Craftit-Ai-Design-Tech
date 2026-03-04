#!/usr/bin/env python3

import re

# Read the current HTML
with open('ai-design-research.html', 'r') as f:
    content = f.read()

def convert_summary_to_narrative(match):
    """Convert bullet-style summary to narrative format"""
    full_summary = match.group(0)
    
    # Extract the linked items 
    links_text = re.search(r'<div style="font-size:0\.85rem.*?">(.*?)</div>', full_summary, re.DOTALL)
    if not links_text:
        return full_summary
    
    links_content = links_text.group(1)
    
    # Extract all the individual links and their text
    link_pattern = r'<a href="([^"]*)"[^>]*>([^<]*)</a>(?:\s*<span class="tag yt">▶ youtube</span>)?'
    links = re.findall(link_pattern, links_content)
    
    if not links:
        return full_summary
    
    # Create narrative based on the links found
    narrative_parts = []
    
    # Group links by theme/category for better narrative flow
    tools = []
    funding = []
    youtube = []
    
    for url, title in links:
        title_lower = title.lower()
        if '▶ youtube' in links_content and url in links_content:
            youtube.append((url, title))
        elif any(word in title_lower for word in ['raises', 'funding', '$', 'million', 'series']):
            funding.append((url, title))
        else:
            tools.append((url, title))
    
    # Build narrative paragraphs
    if tools:
        if len(tools) == 1:
            narrative_parts.append(f'<a href="{tools[0][0]}" style="color:var(--accent);text-decoration:none;">{tools[0][1]}</a> represents a major shift in AI-design integration.')
        else:
            # Create thematic narrative based on content
            tool_links = [f'<a href="{url}" style="color:var(--accent);text-decoration:none;">{title}</a>' for url, title in tools[:3]]
            if 'figma' in ' '.join([title.lower() for _, title in tools]) and 'mcp' in ' '.join([title.lower() for _, title in tools]):
                narrative_parts.append(f'🔥 **Design-to-code convergence:** {tool_links[0]} launches with bidirectional MCP workflow. {" · ".join(tool_links[1:3])} advance the ecosystem further.')
            else:
                narrative_parts.append(f'🔥 **Key developments:** {" · ".join(tool_links)} shape the AI design landscape.')
    
    if funding:
        fund_links = [f'<a href="{url}" style="color:var(--accent);text-decoration:none;">{title}</a>' for url, title in funding[:2]]
        narrative_parts.append(f'💰 **Market momentum:** {" · ".join(fund_links)} signal continued investor confidence in AI design tools.')
    
    if youtube:
        yt_links = [f'<a href="{url}" style="color:var(--accent);text-decoration:none;">{title}</a> <span class="tag yt">▶ youtube</span>' for url, title in youtube[:2]]
        narrative_parts.append(f'📹 **Community insights:** {" · ".join(yt_links)} provide practical implementation guidance.')
    
    # If no clear categorization, just create a simpler narrative
    if not narrative_parts and links:
        all_links = [f'<a href="{url}" style="color:var(--accent);text-decoration:none;">{title}</a>' for url, title in links[:4]]
        narrative_parts.append(f'Key developments include {" · ".join(all_links[:2])}.')
        if len(all_links) > 2:
            narrative_parts.append(f'Additional highlights: {" · ".join(all_links[2:])}.')
    
    # Build the new summary
    narrative_text = ' '.join(narrative_parts) if narrative_parts else links_content
    
    new_summary = f'''<div class="summary" style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:1.5rem;">
<div style="font-size:0.75rem;color:var(--text-tertiary);margin-bottom:0.5rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">📋 Daily Summary</div>
<div style="font-size:0.85rem;line-height:1.8;color:var(--text-secondary);">
{narrative_text}
</div></div>'''
    
    return new_summary

# Pattern to match all summary sections
summary_pattern = r'<div class="summary"[^>]*>.*?<div style="font-size:0\.75rem[^>]*>Today\'s Highlights</div>.*?</div>\s*</div>'

# Count before
original_summaries = len(re.findall(summary_pattern, content, re.DOTALL))

# Convert all summaries
converted_content = re.sub(summary_pattern, convert_summary_to_narrative, content, flags=re.DOTALL)

# Count after
remaining_old = len(re.findall(summary_pattern, converted_content, re.DOTALL))

# Write the converted content
with open('ai-design-research.html', 'w') as f:
    f.write(converted_content)

print(f"Converted {original_summaries - remaining_old} summaries to narrative format")
print(f"Remaining old format: {remaining_old}")

# Count new format
new_format = len(re.findall(r'📋 Daily Summary', converted_content))
print(f"New narrative summaries: {new_format}")