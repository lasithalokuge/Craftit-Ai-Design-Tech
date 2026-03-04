#!/usr/bin/env python3

import re

# Read the current HTML
with open('ai-design-research.html', 'r') as f:
    content = f.read()

# Hand-crafted beautiful summaries based on actual content
summaries = {
    "March 3, 2026": """🔥 **Design-to-code convergence:** <a href="#openai-figma-codex-partnership" style="color:var(--accent);text-decoration:none;">OpenAI Codex + Figma Launch Code-to-Design Integration</a> creates official roundtrip workflows where teams start anywhere (prompt, code, or design) and move forward with speed. <a href="#flora-ai-42m-series-a" style="color:var(--accent);text-decoration:none;">Flora AI's $42M Series A</a> validates node-based AI design approaches used by Alibaba and Pentagram.

💡 **Interactive breakthroughs:** <a href="#mcp-apps-interactive-ui" style="color:var(--accent);text-decoration:none;">MCP Apps</a> enable interactive UIs to render directly inside AI conversations, transforming how design tools integrate with AI agents. Combined with <a href="#figma-design-system-claude-mcp-yt" style="color:var(--accent);text-decoration:none;">complete design system automation</a> <span class="tag yt">▶ youtube</span>, the AI-design pipeline is maturing rapidly.""",

    "March 2, 2026": """🔥 **Bidirectional workflow achieved:** <a href="#figma-codex-integration-tc" style="color:var(--accent);text-decoration:none;">Figma Partners with OpenAI to Integrate Codex</a> via MCP server creates the first official multi-model design hub (Claude Code + OpenAI Codex). <a href="#claude-code-figma-mcp-new-yt" style="color:var(--accent);text-decoration:none;">Push UI Designs from Claude Code BACK to Figma</a> <span class="tag yt">▶ youtube</span> demonstrates true roundtrip capabilities.

🛠️ **Ecosystem expansion:** <a href="#paper-design-shaders" style="color:var(--accent);text-decoration:none;">Paper.design adds GPU shaders + 1M MCP calls/week</a>, while <a href="#stitch-hatter-mcp-export" style="color:var(--accent);text-decoration:none;">Google Stitch introduces Hatter agent</a> with native MCP export. <a href="#pencil-dev-fixes-design-errors-yt" style="color:var(--accent);text-decoration:none;">Pencil.dev + Claude Code</a> <span class="tag yt">▶ youtube</span> shows 90% design error reduction in practice.""",

    "March 1, 2026": """🔥 **Major funding surge:** <a href="#framer-2b-valuation" style="color:var(--accent);text-decoration:none;">Framer hits $2B valuation</a> with 500K+ users and new Wireframer/Workshop AI features. <a href="#openai-730b-funding" style="color:var(--accent);text-decoration:none;">OpenAI raises $110B at $730B valuation</a> — the biggest AI round ever — signaling continued market confidence.

💡 **Infrastructure maturation:** <a href="#mcp-ecosystem-growth" style="color:var(--accent);text-decoration:none;">MCP ecosystem grows</a> as more tools adopt the standard. <a href="#ux-research-ai-native" style="color:var(--accent);text-decoration:none;">UX research stack goes AI-native</a> with Dovetail synthesis and Hotjar behavioral AI integration.""",

    "February 28, 2026": """🔥 **Enterprise AI surge:** <a href="#anthropic-enterprise-agents" style="color:var(--accent);text-decoration:none;">Anthropic Enterprise Agents</a> launch with pre-built design, finance & HR plug-ins. <a href="#webflow-claude-mcp" style="color:var(--accent);text-decoration:none;">Webflow AI + Claude MCP Connector</a> creates direct integration paths for design-to-code workflows.

⚡ **Speed innovations:** <a href="#uxpin-ai-gpt51-claude45" style="color:var(--accent);text-decoration:none;">UXPin AI Component Creator</a> combines GPT-5.1 + Claude Sonnet 4.5 for multi-model component generation. <a href="#vibe-design-claude-figma" style="color:var(--accent);text-decoration:none;">'Vibe Design'</a> emerges as Claude generates complete Figma design systems from single prompts.""",

    "February 27, 2026": """🔥 **Bidirectional breakthrough:** <a href="#figma-openai-codex-yt" style="color:var(--accent);text-decoration:none;">Figma × OpenAI Codex Integration</a> <span class="tag yt">▶ youtube</span> creates the first official design-to-code partnership. <a href="#openai-codex-1m-downloads" style="color:var(--accent);text-decoration:none;">OpenAI Codex MacOS App hits 1M downloads</a> in its first week, validating desktop AI coding demand.

🛠️ **Enterprise momentum:** <a href="#dronahq-vibe-coding" style="color:var(--accent);text-decoration:none;">DronaHQ Vibe Coding</a> targets enterprise AI app development, while <a href="#clark-superblocks-ai-agent" style="color:var(--accent);text-decoration:none;">Clark by Superblocks</a> becomes the first AI agent specifically for enterprise internal apps.""",

    "February 26, 2026": """🔥 **Design-to-code convergence:** <a href="#paper-design-mcp" style="color:var(--accent);text-decoration:none;">Paper.design</a> launches an HTML/CSS-native canvas with a powerful MCP server — AI agents can now read and write design files directly. <a href="#subframe-mcp" style="color:var(--accent);text-decoration:none;">Subframe</a> ships production React code from a visual canvas + CLI sync + MCP. <a href="#stitch-hatter-mcp-export" style="color:var(--accent);text-decoration:none;">Google Stitch adds Hatter agent</a> + native MCP export (free!).

📊 **Market signals:** <a href="#big-tech-650b-ai" style="color:var(--accent);text-decoration:none;">Big Tech to spend $650B on AI in 2026</a> per Bridgewater analysis, while <a href="#fastmcp-gateway" style="color:var(--accent);text-decoration:none;">fastmcp-gateway</a> solves MCP complexity with 3 meta-tools replacing 150+ schemas.""",

    "February 25, 2026": """🔥 **Motion design consolidation:** <a href="#canva-cavalry-mango" style="color:var(--accent);text-decoration:none;">Canva acquires Cavalry + Mango AI</a> for motion design dominance, reaching $4B ARR with 265M users. <a href="#figma-anthropic-multimodel" style="color:var(--accent);text-decoration:none;">Figma's multi-model AI strategy</a> orchestrates GPT-4o + Claude 3 for different tasks.

💰 **Funding surge:** <a href="#krea-ai-83m" style="color:var(--accent);text-decoration:none;">Krea AI raises $83M Series B</a> for unified GenAI creative platforms, while <a href="#mcp-apps-deep" style="color:var(--accent);text-decoration:none;">MCP Apps deep dive</a> reveals 75+ apps with bidirectional UI-AI communication.""",

    "February 24, 2026": """🔥 **Figma-Claude revolution:** <a href="#figma-code-to-canvas" style="color:var(--accent);text-decoration:none;">Figma × Anthropic Code to Canvas</a> launches reverse workflows where Claude Code output becomes editable Figma designs. <a href="#figma-design-system-claude-mcp-yt" style="color:var(--accent);text-decoration:none;">Complete design system automation</a> <span class="tag yt">▶ youtube</span> shows production codebase → Figma components in minutes.

⚡ **Speed breakthroughs:** <a href="#claude-code-figma-roundtrip" style="color:var(--accent);text-decoration:none;">Full roundtrip demos</a> <span class="tag yt">▶ youtube</span> prove bidirectional sync between AI-generated code and Figma edits. <a href="#pencil-dev-claude" style="color:var(--accent);text-decoration:none;">Pencil.dev + Claude Code</a> <span class="tag yt">▶ youtube</span> provides infinite design canvas integration."""
}

def replace_summary(match):
    """Replace summary with beautiful hand-crafted version"""
    full_summary = match.group(0)
    
    # Extract the date from the context around this summary
    # Look for h2 with date before this summary
    before_summary = content[:match.start()]
    date_match = re.search(r'<h2>([^<]+)</h2>(?!.*<h2>)', before_summary)
    
    if date_match:
        date = date_match.group(1)
        if date in summaries:
            new_summary = f'''<div class="summary" style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:1.5rem;">
<div style="font-size:0.75rem;color:var(--text-tertiary);margin-bottom:0.5rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">📋 Daily Summary</div>
<div style="font-size:0.85rem;line-height:1.8;color:var(--text-secondary);">
{summaries[date]}
</div></div>'''
            return new_summary
    
    return full_summary

# Pattern to match current summary sections
summary_pattern = r'<div class="summary"[^>]*>.*?<div style="font-size:0\.75rem[^>]*>📋 Daily Summary</div>.*?</div>\s*</div>'

# Replace all summaries
converted_content = re.sub(summary_pattern, replace_summary, content, flags=re.DOTALL)

# Write the converted content
with open('ai-design-research.html', 'w') as f:
    f.write(converted_content)

print("Updated all summaries to beautiful narrative format")
print(f"Summaries created: {len(summaries)}")