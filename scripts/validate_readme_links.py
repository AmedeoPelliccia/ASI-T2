#!/usr/bin/env python3
"""
Validate README Links

Validates that all anchor links in README.md files point to valid section headers.
This is important because GitHub auto-generates anchors from headers, and special
characters like ·, ‑, &, etc. are removed during anchor generation.

Usage:
  python validate_readme_links.py [readme_path]
  python validate_readme_links.py README.md
  python validate_readme_links.py  # defaults to ./README.md
"""

import re
import sys
from pathlib import Path
from typing import Set, List, Tuple


def github_anchor_from_header(header_text: str) -> str:
    """
    Convert a markdown header to GitHub's auto-generated anchor format.
    
    GitHub anchor generation rules:
    1. Convert to lowercase
    2. Remove markdown formatting (links, code blocks)
    3. Remove special Unicode characters (·, ‑, &, —, etc.)
    4. Remove most punctuation except hyphens
    5. Replace spaces with hyphens
    6. Collapse multiple hyphens to single hyphen
    """
    anchor = header_text.lower()
    
    # Remove markdown links: [text](url) -> text
    anchor = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', anchor)
    
    # Remove code formatting: `code` -> code
    anchor = re.sub(r'`([^`]+)`', r'\1', anchor)
    
    # Remove special Unicode characters that GitHub strips
    special_chars = ['·', '‑', '&', '—', '–', '«', '»', '"', '"', ''', ''']
    for char in special_chars:
        anchor = anchor.replace(char, '')
    
    # Remove emoji and other non-alphanumeric chars except space and hyphen
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    
    # Replace sequences of spaces/hyphens with single hyphen
    anchor = re.sub(r'[\s-]+', '-', anchor.strip())
    
    return anchor


def extract_headers(content: str) -> Set[str]:
    """Extract all section headers from markdown and generate their anchors."""
    headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
    return {github_anchor_from_header(h) for h in headers}


def extract_anchor_links(content: str) -> List[Tuple[str, str, int]]:
    """Extract all anchor links from markdown with line numbers."""
    anchor_links = []
    for match in re.finditer(r'\[([^\]]+)\]\(#([^\)]+)\)', content):
        link_text = match.group(1)
        anchor = match.group(2)
        line_num = content[:match.start()].count('\n') + 1
        anchor_links.append((link_text, anchor, line_num))
    return anchor_links


def validate_readme_links(readme_path: Path) -> Tuple[int, int]:
    """
    Validate all anchor links in a README file.
    
    Returns:
        Tuple of (total_links, broken_links)
    """
    if not readme_path.exists():
        print(f"❌ ERROR: {readme_path} does not exist")
        return 0, 0
    
    content = readme_path.read_text(encoding='utf-8')
    
    # Get valid anchors from headers
    valid_anchors = extract_headers(content)
    
    # Get all anchor references
    anchor_links = extract_anchor_links(content)
    
    print(f"🔗 Validating anchor links in {readme_path}")
    print("=" * 80)
    
    broken_links = []
    for link_text, anchor, line_num in anchor_links:
        if anchor in valid_anchors:
            print(f"✅ Line {line_num:3d}: [{link_text}](#{anchor})")
        else:
            print(f"❌ Line {line_num:3d}: [{link_text}](#{anchor}) - BROKEN!")
            broken_links.append((link_text, anchor, line_num))
    
    print("=" * 80)
    
    if broken_links:
        print(f"\n❌ Found {len(broken_links)} broken anchor links:")
        for link_text, anchor, line_num in broken_links:
            print(f"  Line {line_num}: #{anchor}")
        print(f"\nValid anchors available:")
        for anchor in sorted(valid_anchors):
            print(f"  #{anchor}")
        return len(anchor_links), len(broken_links)
    else:
        print(f"✅ SUCCESS: All {len(anchor_links)} anchor links are valid!")
        return len(anchor_links), 0


def main():
    if len(sys.argv) > 1:
        readme_path = Path(sys.argv[1])
    else:
        readme_path = Path("README.md")
    
    total, broken = validate_readme_links(readme_path)
    
    if broken > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
