#!/usr/bin/env python3

import re

# Read the current HTML
with open('ai-design-research.html', 'r') as f:
    content = f.read()

# Extract finding IDs for each day section
day_sections = {}
current_date = None
current_findings = []

# Find all day sections and their findings
day_pattern = r'<h2>(.*?, \d{4})</h2>.*?(?=<h2>|$)'
for day_match in re.finditer(day_pattern, content, re.DOTALL):
    date = day_match.group(1)
    day_content = day_match.group(0)
    
    # Extract finding IDs from this day
    finding_ids = re.findall(r'id="([^"]*)"', day_content)
    # Remove non-finding IDs
    finding_ids = [id for id in finding_ids if id not in ['total-count', 'start-date', 'last-update']]
    
    day_sections[date] = finding_ids
    print(f"{date}: {len(finding_ids)} findings")
    if finding_ids:
        print(f"  First few: {finding_ids[:3]}")

# Corrected summaries with proper links to each day's actual findings
corrected_summaries = {
    "March 2, 2026": """🔥 **Bidirectional workflow achieved:** <a href="#figma-codex-integration-tc" style="color:var(--accent);text-decoration:none;">Figma Partners with OpenAI to Integrate Codex</a> via MCP server creates the first official multi-model design hub (Claude Code + OpenAI Codex). <a href="#claude-code-figma-mcp-new-yt" style="color:var(--accent);text-decoration:none;">Push UI Designs from Claude Code BACK to Figma</a> <span class="tag yt">▶ youtube</span> demonstrates true roundtrip capabilities.

🛠️ **Ecosystem expansion:** <a href="#paper-design-shaders" style="color:var(--accent);text-decoration:none;">Paper.design adds GPU shaders + 1M MCP calls/week</a>, while <a href="#stitch-hatter-mcp-export" style="color:var(--accent);text-decoration:none;">Google Stitch introduces Hatter agent</a> with native MCP export. <a href="#pencil-dev-fixes-design-errors-yt" style="color:var(--accent);text-decoration:none;">Pencil.dev + Claude Code</a> <span class="tag yt">▶ youtube</span> shows 90% design error reduction in practice.""",

    "March 1, 2026": """🔥 **Major funding surge:** <a href="#framer-2b-valuation" style="color:var(--accent);text-decoration:none;">Framer hits $2B valuation</a> with 500K+ users and new Wireframer/Workshop AI features. <a href="#openai-730b-funding" style="color:var(--accent);text-decoration:none;">OpenAI raises $110B at $730B valuation</a> — the biggest AI round ever — signaling continued market confidence.

💡 **Infrastructure maturation:** <a href="#mcp-ecosystem-growth" style="color:var(--accent);text-decoration:none;">MCP ecosystem grows</a> as more tools adopt the standard. <a href="#ux-research-ai-native" style="color:var(--accent);text-decoration:none;">UX research stack goes AI-native</a> with Dovetail synthesis and Hotjar behavioral AI integration."""
}

def replace_summary_with_correct_links(match):
    """Replace summary with corrected links"""
    full_summary = match.group(0)
    
    # Find the date for this summary by looking backwards
    before_summary = content[:match.start()]
    date_match = re.search(r'<h2>([^<]+)</h2>(?!.*<h2>)', before_summary)
    
    if date_match:
        date = date_match.group(1)
        if date in corrected_summaries:
            new_summary = f'''<div class="summary" style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:1.5rem;">
<div style="font-size:0.75rem;color:var(--text-tertiary);margin-bottom:0.5rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">📋 Daily Summary</div>
<div style="font-size:0.85rem;line-height:1.8;color:var(--text-secondary);">
{corrected_summaries[date]}
</div></div>'''
            return new_summary
    
    return full_summary

# Pattern to match current summary sections
summary_pattern = r'<div class="summary"[^>]*>.*?📋 Daily Summary</div>.*?</div>\s*</div>'

# Replace problematic summaries
converted_content = re.sub(summary_pattern, replace_summary_with_correct_links, content, flags=re.DOTALL)

# Write the corrected content
with open('ai-design-research.html', 'w') as f:
    f.write(converted_content)

print("\nCorrected March summaries with proper links")