#!/usr/bin/env python3

import json
from datetime import datetime
from collections import defaultdict

# Read the JSON data
with open('known-findings.json') as f:
    data = json.load(f)

# Group findings by date
by_date = defaultdict(list)
for finding in data['findings']:
    date = finding.get('date', 'unknown')
    if date != 'unknown':
        by_date[date].append(finding)

def generate_complete_day_section(date, findings_for_date):
    """Generate a complete day section with ALL findings"""
    
    # Convert date for display
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    display_date = date_obj.strftime('%B %d, %Y')
    
    # Generate summary based on actual findings
    summaries = {
        "2026-03-15": """🔥 **Design workflow revolution:** <a href="#figma-weave-acquisition" style="color:var(--accent);text-decoration:none;">Figma acquires Weavy for AI generative design integration</a>, while <a href="#shadcn-cli-v4-ai-agents" style="color:var(--accent);text-decoration:none;">shadcn/ui CLI v4 brings AI agent skills</a> to component development. <a href="#openai-gpt-54-computer-use" style="color:var(--accent);text-decoration:none;">OpenAI GPT-5.4 adds native computer use mode</a> for direct interface control.""",
        
        "2026-03-14": """🔥 **Practical AI design adoption:** <a href="#ai-design-workflow-2026-practical" style="color:var(--accent);text-decoration:none;">Real-world AI design workflow tutorials</a> and <a href="#design-system-4-hours-ai" style="color:var(--accent);text-decoration:none;">4-hour design system builds with AI</a> <span class="tag yt">▶ youtube</span> demonstrate practical implementation. <a href="#storybook-9-ai-assistant" style="color:var(--accent);text-decoration:none;">Storybook 9 AI Assistant</a> automates component generation and testing.""",
        
        "2026-03-13": """🔥 **Conference and education focus:** <a href="#into-design-systems-2026-conference" style="color:var(--accent);text-decoration:none;">Into Design Systems Conference 2026</a> reveals industry-wide AI adoption with sessions from major tech companies. <a href="#claude-code-designers-guide" style="color:var(--accent);text-decoration:none;">Claude Code for Designers</a> empowers non-developers to build beyond static screens.""",
        
        "2026-03-12": """🔥 **Enterprise tool integration:** <a href="#coreldraw-2026-ai-integration" style="color:var(--accent);text-decoration:none;">CorelDRAW Graphics Suite 2026</a> adds major AI integration with Artist Intelligence, while <a href="#wispr-flow-android-techcrunch" style="color:var(--accent);text-decoration:none;">Wispr Flow launches Android app</a> with TechCrunch coverage. <a href="#figr-ai-product-hunt-top" style="color:var(--accent);text-decoration:none;">Figr AI tops Product Hunt</a> as product-aware UX agent."""
    }
    
    summary_content = summaries.get(date, f"""💡 **Research completed:** {len(findings_for_date)} findings covering AI design developments, workflow improvements, and tool updates across the design technology landscape.""")
    
    # Group findings by category
    categories = defaultdict(list)
    for f in findings_for_date:
        cat = f.get('category', 'hot')
        categories[cat].append(f)
    
    # Build the section
    html = f'''  <div class="day-section">
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

'''
    
    # Category mappings
    cat_labels = {
        'hot': ('🔥 Hot Finds', 'hot'),
        'tip': ('⚡ Speed Tips', 'tip'),
        'try': ('🛠️ Tool Updates', 'try'),
        'radar': ('🔮 On the Radar', 'radar')
    }
    
    # Add categories in order
    for cat_key in ['hot', 'tip', 'try', 'radar']:
        if cat_key in categories and categories[cat_key]:
            cat_name, cat_class = cat_labels[cat_key]
            html += f'''<div class="category">
<div class="category-label {cat_class}">{cat_name}</div>

'''
            
            for finding in categories[cat_key]:
                # Extract fields with defaults
                title = finding.get('title', 'Research Finding')
                url = finding.get('url', '#')
                description = finding.get('description', f'AI design research finding from {display_date}. Details preserved in research database.')
                verdict = finding.get('verdict', 'Watch')
                tags = finding.get('tags', [])
                
                # Generate clean ID from title
                clean_id = title.lower().replace(' ', '-').replace('—', '').replace(':', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')[:50]
                
                # Determine verdict class
                verdict_class = 'watch'
                if 'try' in verdict.lower() or 'practical' in verdict.lower():
                    verdict_class = 'try'
                elif 'skip' in verdict.lower():
                    verdict_class = 'skip'
                
                # Extract domain from URL
                if url and url != '#':
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc.replace('www.', '') if url != '#' else 'research-database'
                else:
                    domain = 'research-database'
                
                html += f'''      <div class="finding">
        <div class="finding-header">
          <h4><a href="{url}" target="_blank" id="{clean_id}">{title}</a></h4>
          <span class="verdict {verdict_class}">{verdict}</span>
        </div>
        <div class="source-url"><a href="{url}" target="_blank">{domain}</a></div>
        <p class="desc">{description}</p>
        <div class="finding-footer">
          <div class="tags">
'''
                # Add tags
                for tag in tags:
                    html += f'            <span class="tag">{tag}</span>\n'
                    
                html += '''          </div>
        </div>
      </div>

'''
            
            html += '''    </div>

'''
    
    html += '''  </div>

'''
    return html

# Generate sections for recent dates
target_dates = ['2026-03-15', '2026-03-14', '2026-03-13', '2026-03-12']

for date in target_dates:
    if date in by_date:
        findings = by_date[date]
        section_html = generate_complete_day_section(date, findings)
        
        # Write to file
        filename = f"complete-{date}.html"
        with open(filename, 'w') as f:
            f.write(section_html)
            
        print(f"✅ Generated {filename} with ALL {len(findings)} findings")

print(f"\n🎯 Ready to replace incomplete sections with complete ones!")