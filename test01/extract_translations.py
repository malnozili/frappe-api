#!/usr/bin/env python3
"""
Script to extract all translatable messages from the project
Extracts _() from Python files and __() from JavaScript/HTML files
"""

import os
import re
import csv
from pathlib import Path

def extract_python_translations(file_path):
    """Extract _() translations from Python files"""
    translations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all _("...") patterns
        pattern = r'_\("([^"]*)"\)'
        matches = re.findall(pattern, content)
        
        for match in matches:
            if match.strip():
                translations.append({
                    'source': match,
                    'file': str(file_path),
                    'type': 'python'
                })
                
        # Find all _('...') patterns
        pattern = r"_\('([^']*)'\)"
        matches = re.findall(pattern, content)
        
        for match in matches:
            if match.strip():
                translations.append({
                    'source': match,
                    'file': str(file_path),
                    'type': 'python'
                })
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return translations

def extract_js_translations(file_path):
    """Extract __() translations from JavaScript/HTML files"""
    translations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all __("...") patterns
        pattern = r'__\("([^"]*)"\)'
        matches = re.findall(pattern, content)
        
        for match in matches:
            if match.strip():
                translations.append({
                    'source': match,
                    'file': str(file_path),
                    'type': 'javascript'
                })
                
        # Find all __('...') patterns
        pattern = r"__\('([^']*)'\)"
        matches = re.findall(pattern, content)
        
        for match in matches:
            if match.strip():
                translations.append({
                    'source': match,
                    'file': str(file_path),
                    'type': 'javascript'
                })
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return translations

def extract_html_translations(file_path):
    """Extract translations from HTML template files"""
    translations = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all {{ _("...") }} patterns
        pattern = r'\{\{\s*_\("([^"]*)"\)\s*\}\}'
        matches = re.findall(pattern, content)
        
        for match in matches:
            if match.strip():
                translations.append({
                    'source': match,
                    'file': str(file_path),
                    'type': 'html'
                })
                
        # Find all {{ __("...") }} patterns
        pattern = r'\{\{\s*__\("([^"]*)"\)\s*\}\}'
        matches = re.findall(pattern, content)
        
        for match in matches:
            if match.strip():
                translations.append({
                    'source': match,
                    'file': str(file_path),
                    'type': 'html'
                })
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return translations

def scan_directory(directory):
    """Scan directory recursively for translatable messages"""
    all_translations = []
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv']]
        
        for file in files:
            file_path = Path(root) / file
            
            # Process Python files
            if file.endswith('.py'):
                translations = extract_python_translations(file_path)
                all_translations.extend(translations)
                
            # Process JavaScript files
            elif file.endswith('.js'):
                translations = extract_js_translations(file_path)
                all_translations.extend(translations)
                
            # Process HTML files
            elif file.endswith('.html'):
                translations = extract_html_translations(file_path)
                all_translations.extend(translations)
    
    return all_translations

def create_translation_csv(translations, output_file):
    """Create CSV file with translations"""
    # Remove duplicates while preserving order
    seen = set()
    unique_translations = []
    
    for trans in translations:
        if trans['source'] not in seen:
            seen.add(trans['source'])
            unique_translations.append(trans)
    
    # Sort by source text
    unique_translations.sort(key=lambda x: x['source'])
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source', 'target', 'context', 'file', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for trans in unique_translations:
            writer.writerow({
                'source': trans['source'],
                'target': '',  # Empty for manual translation
                'context': f"Found in {trans['file']} ({trans['type']})",
                'file': trans['file'],
                'type': trans['type']
            })
    
    return len(unique_translations)

def main():
    """Main function"""
    # Get the project root directory
    project_root = Path(__file__).parent
    
    print(f"Scanning for translations in: {project_root}")
    
    # Scan for translations
    translations = scan_directory(project_root)
    
    # Create output directory if it doesn't exist
    output_dir = project_root / 'translations'
    output_dir.mkdir(exist_ok=True)
    
    # Create comprehensive translation file
    output_file = output_dir / 'extracted_translations.csv'
    count = create_translation_csv(translations, output_file)
    
    print(f"\nFound {count} unique translatable messages")
    print(f"Translation file created: {output_file}")
    
    # Create summary
    summary_file = output_dir / 'translation_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Translation Extraction Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total unique messages found: {count}\n\n")
        
        # Group by type
        by_type = {}
        for trans in translations:
            t_type = trans['type']
            if t_type not in by_type:
                by_type[t_type] = []
            by_type[t_type].append(trans['source'])
        
        for t_type, messages in by_type.items():
            f.write(f"{t_type.upper()} messages ({len(messages)}):\n")
            for msg in sorted(set(messages)):
                f.write(f"  - {msg}\n")
            f.write("\n")
    
    print(f"Summary file created: {summary_file}")
    
    # Show some examples
    print("\nExample translations found:")
    for i, trans in enumerate(translations[:10]):
        print(f"  {i+1}. {trans['source']} ({trans['type']})")
    
    if len(translations) > 10:
        print(f"  ... and {len(translations) - 10} more")

if __name__ == "__main__":
    main()
