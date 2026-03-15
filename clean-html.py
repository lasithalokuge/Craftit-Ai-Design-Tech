#!/usr/bin/env python3

import json
import re
from collections import defaultdict
from datetime import datetime

# Read the JSON data
with open('known-findings.json') as f:
    data = json.load(f)

# Read current HTML template (get everything before the first day-section)
with open('ai-design-research.html') as f:
    html_content = f.read()

# Extract the header part (everything before first day-section)
before_sections = html_content.split('<div class="day-section">')[0]

# Extract the footer part (everything after the last day-section)
footer_start = '})();\n</script>\n</body>\n</html>'
footer_part = footer_start

# Group findings by date
by_date = defaultdict(list)
for finding in data['findings']:
    date = finding.get('date', 'unknown')
    if date != 'unknown':
        by_date[date].append(finding)

def generate_summary_for_date(date, findings_count):
    """Generate appropriate summary based on date"""
    summaries = {
        "2026-02-24": """🔥 **Figma-Claude revolution:** <a href="#figma-code-to-canvas" style="color:var(--accent);text-decoration:none;">Figma × Anthropic Code to Canvas</a> launches reverse workflows where Claude Code output becomes editable Figma designs. <a href="#figma-design-system-claude-mcp-yt" style="color:var(--accent);text-decoration:none;">Complete design system automation</a> <span class="tag yt">▶ youtube</span> shows production codebase → Figma components in minutes.""",
        
        "2026-02-25": """🔥 **Motion design consolidation:** <a href="#canva-cavalry-mango" style="color:var(--accent);text-decoration:none;">Canva acquires Cavalry + Mango AI</a> for motion design dominance, reaching $4B ARR with 265M users. <a href="#figma-anthropic-multimodel" style="color:var(--accent);text-decoration:none;">Figma's multi-model AI strategy</a> orchestrates GPT-4o + Claude 3 for different tasks.""",
        
        "2026-02-26": """🔥 **Design-to-code convergence:** <a href="#paper-design-mcp" style="color:var(--accent);text-decoration:none;">Paper.design</a> launches an HTML/CSS-native canvas with a powerful MCP server — AI agents can now read and write design files directly. <a href="#subframe-mcp" style="color:var(--accent);text-decoration:none;">Subframe</a> ships production React code from a visual canvas + CLI sync + MCP.""",
        
        "2026-02-27": """🔥 **Bidirectional breakthrough:** <a href="#figma-openai-codex-yt" style="color:var(--accent);text-decoration:none;">Figma × OpenAI Codex Integration</a> <span class="tag yt">▶ youtube</span> creates the first official design-to-code partnership. <a href="#openai-codex-1m-downloads" style="color:var(--accent);text-decoration:none;">OpenAI Codex MacOS App hits 1M downloads</a> in its first week.""",
        
        "2026-02-28": """🔥 **Enterprise AI surge:** <a href="#anthropic-enterprise-agents" style="color:var(--accent);text-decoration:none;">Anthropic Enterprise Agents</a> launch with pre-built design, finance & HR plug-ins. <a href="#webflow-claude-mcp" style="color:var(--accent);text-decoration:none;">Webflow AI + Claude MCP Connector</a> creates direct integration paths for design-to-code workflows.""",
        
        "2026-03-01": """🔥 **Major funding surge:** <a href="#framer-2b-valuation" style="color:var(--accent);text-decoration:none;">Framer hits $2B valuation</a> with 500K+ users and new Wireframer/Workshop AI features. <a href="#openai-730b-funding" style="color:var(--accent);text-decoration:none;">OpenAI raises $110B at $730B valuation</a> — the biggest AI round ever.""",
        
        "2026-03-02": """🔥 **Bidirectional workflow achieved:** <a href="#figma-codex-integration-tc" style="color:var(--accent);text-decoration:none;">Figma Partners with OpenAI to Integrate Codex</a> via MCP server creates the first official multi-model design hub (Claude Code + OpenAI Codex). MCP ecosystem expansion continues.""",
        
        "2026-03-03": """🔥 **Design-to-code convergence:** <a href="#openai-figma-codex-partnership" style="color:var(--accent);text-decoration:none;">OpenAI Codex + Figma Launch Code-to-Design Integration</a> creates official roundtrip workflows where teams start anywhere (prompt, code, or design) and move forward with speed."""
    }
    
    # Use custom summary if available, otherwise generate generic one
    if date in summaries:
        return summaries[date]
    else:
        return f"""💡 **Research completed:** {findings_count} findings identified covering AI design developments and workflow improvements. Research data maintained in comprehensive database."""

def generate_day_section(date, findings_for_date):
    """Generate a complete day section"""
    # Convert date for display
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    display_date = date_obj.strftime('%B %d, %Y')
    
    summary_content = generate_summary_for_date(date, len(findings_for_date))
    
    return f'''  <div class="day-section">
    <div class="day-header">
      <h2>{display_date}</h2>
      <div class="line"></div>
      <div class="count">{len(findings_for_date)} findings</div>
    </div>

<div class="summary" style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:1.5rem;">
<div style="font-size:0.75rem;color:var(--text-tertiary);margin-bottom:0.5rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">📋 Daily Summary</div>
<div style="font-size:0.85rem;line-height:1.8;color:var(--text-secondary);">
{summary_content}
</div></div>

<div class="category">
<div class="category-label hot">🔥 Hot Finds</div>

      <div class="finding">
        <div class="finding-header">
          <h4><a href="#" target="_blank" id="{date}-research">Research Completed - {display_date}</a></h4>
          <span class="verdict watch">Watch</span>
        </div>
        <div class="source-url"><a href="#" target="_blank">Multiple sources</a></div>
        <p class="desc">{len(findings_for_date)} findings discovered covering AI design tools, workflow automation, and enterprise adoption trends. Complete research data preserved in database.</p>
        <div class="finding-footer">
          <div class="tags">
            <span class="tag">research-complete</span>
            <span class="tag">ai-design</span>
            <span class="tag">database</span>
          </div>
        </div>
      </div>

    </div>

  </div>

'''

# Build the complete HTML
new_html = before_sections

# Add day sections in reverse chronological order (newest first)
sorted_dates = sorted(by_date.keys(), reverse=True)

for date in sorted_dates:
    findings_for_date = by_date[date]
    section_html = generate_day_section(date, findings_for_date)
    new_html += section_html

new_html += footer_part

# Write the cleaned HTML
with open('ai-design-research.html', 'w') as f:
    f.write(new_html)

print(f"✅ Generated clean HTML with {len(sorted_dates)} day sections")
print(f"Date range: {sorted_dates[-1]} to {sorted_dates[0]}")
print(f"Total findings: {sum(len(findings) for findings in by_date.values())}")