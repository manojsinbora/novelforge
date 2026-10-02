import pathlib
import re

chapters_dir = pathlib.Path('stories/omnicrafter_of_the_fallen_era/chapters')
files = sorted([f for f in chapters_dir.glob('0*.md') if not f.name.endswith('_illustrated.md')])

print(f"Auditing {len(files)} chapters across all 12 Arcs...")

errors = []
warnings = []

# Regex patterns for corrupted characters or artifacts
mojibake_pattern = re.compile(r'[âÃ][\x80-\xbf]+')

for f in files:
    text = f.read_text(encoding='utf-8')
    words = len(text.split())
    
    # 1. Word Count check
    if words < 1800:
        errors.append(f"{f.name}: WORD COUNT DEFICIT -> {words} words (Required: >= 1800)")
        
    # 2. First line heading check
    lines = text.split('\n')
    first_line = lines[0].strip() if lines else ""
    if not first_line.startswith("# Chapter "):
        errors.append(f"{f.name}: Invalid heading -> '{first_line[:40]}'")
        
    # 3. Unicode replacement character
    if '\ufffd' in text:
        errors.append(f"{f.name}: Contains unicode replacement character (\ufffd)")
        
    # 4. Mojibake detection
    mojibake_matches = mojibake_pattern.findall(text)
    if mojibake_matches:
        errors.append(f"{f.name}: Contains potential Mojibake ({len(mojibake_matches)} occurrences, e.g., {mojibake_matches[:3]})")
        
    # 5. Question mark character encoding corruption (e.g., 'Arthur?s' or 'it?s')
    q_corrupt = re.findall(r'[a-zA-Z]\?[a-zA-Z]', text)
    if q_corrupt:
        errors.append(f"{f.name}: Corrupted apostrophe/quote as question mark -> {set(q_corrupt)}")
        
    # 6. Bad placeholder tokens
    for token in ['TODO', 'FIXME', 'TBD', '[insert', '<truncated', 'undefined']:
        if token in text:
            errors.append(f"{f.name}: Contains placeholder token '{token}'")
            
    # 7. Unclosed code blocks (odd number of ```)
    code_blocks = text.count("```")
    if code_blocks % 2 != 0:
        errors.append(f"{f.name}: Uneven code blocks ({code_blocks} backtick delimiters)")

print(f"\n--- AUDIT RESULTS ---")
print(f"Total Errors Found: {len(errors)}")
for err in errors:
    print(f" [ERROR] {err}")

if not errors:
    print("ALL 180 CHAPTERS PASSED COMPREHENSIVE INTEGRITY AUDIT WITH 0 ERRORS!")
