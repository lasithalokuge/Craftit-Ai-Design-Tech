#!/usr/bin/env python3

import json
from collections import defaultdict

# Read the JSON data
with open('known-findings.json') as f:
    data = json.load(f)

findings = data['findings']

# Group findings by date
by_date = defaultdict(list)
for finding in findings:
    date = finding.get('date', 'unknown')
    if date != 'unknown':
        by_date[date].append(finding)

# Generate HTML sections for March 12-15
missing_dates = ['2026-03-15', '2026-03-14', '2026-03-13', '2026-03-12']

def generate_day_section(date, findings_for_date):
    # Convert date for display
    from datetime import datetime
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    display_date = date_obj.strftime('%B %d, %Y')
    
    # Group by category
    categories = defaultdict(list)
    for f in findings_for_date:
        cat = f.get('category', 'hot')
        categories[cat].append(f)
    
    # Build HTML
    html = f'''  <div class="day-section">
    <div class="day-header">
      <h2>{display_date}</h2>
      <div class="line"></div>
      <div class="count">{len(findings_for_date)} findings</div>
    </div>

<div class="summary" style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:1.5rem;">
<div style="font-size:0.75rem;color:var(--text-tertiary);margin-bottom:0.5rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">📋 Daily Summary</div>
<div style="font-size:0.85rem;line-height:1.8;color:var(--text-secondary);">
🔥 **Research findings for {display_date}:** {len(findings_for_date)} new tools and developments discovered across AI design, workflow automation, and enterprise adoption trends.
</div></div>

'''
    
    # Category mappings
    cat_labels = {
        'hot': ('🔥 Hot Finds', 'hot'),
        'tip': ('⚡ Speed Tips', 'tip'), 
        'try': ('🛠️ Tool Updates', 'try'),
        'radar': ('🔮 On the Radar', 'radar')
    }
    
    for cat_key in ['hot', 'tip', 'try', 'radar']:
        if cat_key in categories:
            cat_name, cat_class = cat_labels[cat_key]
            html += f'''<div class="category">
<div class="category-label {cat_class}">{cat_name}</div>

'''
            for finding in categories[cat_key]:
                # Determine verdict
                verdict_text = finding.get('verdict', 'Watch')
                verdict_class = 'watch'
                if 'try' in verdict_text.lower() or 'practical' in verdict_text.lower():
                    verdict_class = 'try'
                elif 'skip' in verdict_text.lower():
                    verdict_class = 'skip'
                    
                # Clean URL for source
                url = finding.get('url', '#')
                from urllib.parse import urlparse
                domain = urlparse(url).netloc.replace('www.', '') if url != '#' else 'unknown'
                
                # Generate ID from title
                finding_id = finding.get('id', finding['title'].lower().replace(' ', '-').replace('—', '').replace(':', '')[:50])
                
                html += f'''      <div class="finding">
        <div class="finding-header">
          <h4><a href="{url}" target="_blank" id="{finding_id}">{finding['title']}</a></h4>
          <span class="verdict {verdict_class}">{verdict_text}</span>
        </div>
        <div class="source-url"><a href="{url}" target="_blank">{domain}</a></div>
        <p class="desc">{finding['description']}</p>
        <div class="finding-footer">
          <div class="tags">
'''
                # Add tags
                tags = finding.get('tags', [])
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

# Generate sections for missing dates
for date in missing_dates:
    if date in by_date:
        findings_for_date = by_date[date]
        section_html = generate_day_section(date, findings_for_date)
        
        # Write to file
        filename = f"{date}-section.html"
        with open(filename, 'w') as f:
            f.write(section_html)
        
        print(f"Generated {filename} with {len(findings_for_date)} findings")

print(f"\nTotal findings available: {len(findings)}")
print(f"Dates with data: {len(by_date)}")