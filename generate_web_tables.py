#!/usr/bin/env python3
import os
import re

def parse_typst_dictionary():
    dict_path = "src/maligavero/bukenkango.typ"
    if not os.path.exists(dict_path):
        return []
        
    with open(dict_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Locate individual dictionary blocks enclosed by ( ... )
    # This matches the structure of your typed entries perfectly
    entries_raw = re.findall(r'\(\s*(en:.*?)\s*\),', content, re.DOTALL)
    
    parsed_entries = []
    for entry in entries_raw:
        data = {}
        # Parse text fields extraction
        for field in ['en', 'rk', 'pos', 'category', 'def', 'rk-def', 'example', 'note']:
            match = re.search(r'' + field + r':\s*"(.*?)"', entry)
            if match:
                data[field] = match.group(1)
        
        # Pseudo-parse math equations (convert Typst $F/A$ format to MkDocs Material math blocks)
        eq_match = re.search(r'equation:\s*\$(.*?)\$', entry)
        if eq_match:
            raw_eq = eq_match.group(1).strip()
            # Basic fallback formatting for the web viewer
            data['equation'] = f"<code>{raw_eq}</code>"
        else:
            data['equation'] = "N/A"
            
        if 'en' in data and 'rk' in data:
            parsed_entries.append(data)
            
    return parsed_entries

def build_markdown_table(terms, title):
    md = f"# {title}\n\n"
    md += "| Term (EN) | Extended Rukwangali | Pos | Definition (EN / RK) | Formula / Notes |\n"
    md += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for t in terms:
        eq_or_note = t['equation'] if t['equation'] != "N/A" else f"<small>{t.get('note', '')}</small>"
        md += f"| **{t['en']}** | `{t['rk']}` | *{t['pos']}* | **EN:** {t['def']}<br>**RK:** {t['rk-def']}<br><small>_Example:_ {t.get('example','')}</small> | {eq_or_note} |\n"
    return md

def main():
    terms = parse_typst_dictionary()
    
    # Domain router map linking your folder structures to matching categories
    domains = {
        "muvaru": "Mathematics",
        "ediwomutji": "Chemistry",
        "ediwonsitwe": "Physics",
        "yokompiuta": "Computing",
        "upangerera": "Engineering",
        "ediwomwenyo": "Biology"
    }
    
    for folder, category_keyword in domains.items():
        # Match if the keyword exists inside the multi-value category block
        matched_terms = [t for t in terms if category_keyword.lower() in t['category'].lower()]
        
        # If no entries are found yet, keep a generic helpful placeholder message
        if not matched_terms:
            md_content = f"# {category_keyword} Technical Register\n\nNo terms registered yet. Populate your `src/maligavero/bukenkango.typ` using the `{category_keyword}` category tag."
        else:
            md_content = build_markdown_table(matched_terms, f"{category_keyword} Technical Register")
            
        # Safely rewrite the live document index for the domain
        with open(f"docs/{folder}/index.md", "w", encoding="utf-8") as out:
            out.write(md_content)
            
    print("✓ Web documentation tracks synchronized with master Typst dictionary successfully.")

if __name__ == "__main__":
    main()

