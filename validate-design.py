#!/usr/bin/env python3
"""
Design Format Validator
Checks if HTML matches the expected beautiful format before going live.
"""

import re
import sys

def validate_design_format(html_file):
    """Check if the HTML follows the correct design format"""
    
    with open(html_file, 'r') as f:
        content = f.read()
    
    errors = []
    
    # Check 1: Findings should use h4 in finding-header, not h3
    # Look specifically for h3 tags within finding divs
    finding_pattern = r'<div class="finding"[^>]*>.*?</div>\s*</div>'
    findings = re.findall(finding_pattern, content, re.DOTALL)
    h3_in_findings = 0
    for finding in findings:
        if '<h3>' in finding:
            h3_in_findings += 1
    
    if h3_in_findings > 0:
        errors.append(f"❌ Found {h3_in_findings} finding cards using <h3> instead of <h4>")
    
    # Check 2: Verdict should be span.verdict, not text
    text_verdicts = re.findall(r'<span class="verdict">[^<]*</span>', content)
    if len(text_verdicts) == 0:  # No verdict spans found
        text_verdict_patterns = re.findall(r'<p[^>]*><strong>Verdict:</strong>', content)
        if text_verdict_patterns:
            errors.append(f"❌ Found {len(text_verdict_patterns)} text verdicts instead of verdict badges")
    
    # Check 3: Should have finding-header structure
    proper_headers = re.findall(r'<div class="finding-header">', content)
    total_findings = re.findall(r'<div class="finding"[^>]*>', content)
    
    if len(proper_headers) != len(total_findings):
        errors.append(f"❌ {len(total_findings)} findings but only {len(proper_headers)} proper headers")
    
    # Check 4: Should have colored verdict badges
    verdict_badges = re.findall(r'<span class="verdict [^"]*">', content)
    if len(verdict_badges) < len(total_findings):
        errors.append(f"❌ Missing colored verdict badges: {len(verdict_badges)}/{len(total_findings)}")
    
    # Check 5: Should have finding-footer with tags
    footers = re.findall(r'<div class="finding-footer">', content)
    if len(footers) != len(total_findings):
        errors.append(f"❌ Missing finding-footer: {len(footers)}/{len(total_findings)}")
    
    return errors

if __name__ == '__main__':
    html_file = sys.argv[1] if len(sys.argv) > 1 else 'ai-design-research.html'
    
    errors = validate_design_format(html_file)
    
    if errors:
        print("🚨 DESIGN FORMAT ERRORS DETECTED:")
        for error in errors:
            print(f"  {error}")
        print("\n❌ VALIDATION FAILED - DO NOT MERGE TO MAIN")
        sys.exit(1)
    else:
        print("✅ DESIGN FORMAT VALIDATION PASSED")
        print("✅ Safe to merge to main branch")
        sys.exit(0)