#!/usr/bin/env python3
"""Fix encoding issues in Python examples for Windows compatibility."""

import sys
import re
from pathlib import Path

# Fix template
FIX_CODE = """
import asyncio
import sys
import io
from pathlib import Path

# Configurar stdout para UTF-8 (necessário no Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""

def fix_file(filepath):
    """Add UTF-8 encoding fix to a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already fixed
    if 'sys.stdout = io.TextIOWrapper' in content:
        return False
    
    # Find the import section and add the fix
    # Match: import asyncio, import sys, from pathlib import Path
    pattern = r'(import asyncio\s*\nimport sys\s*\nfrom pathlib import Path)'
    
    replacement = r'''import asyncio
import sys
import io
from pathlib import Path

# Configurar stdout para UTF-8 (necessário no Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')'''
    
    new_content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

# Fix all Python examples
examples_dir = Path(__file__).parent
python_files = list(examples_dir.glob("**/*.py"))

for filepath in python_files:
    if fix_file(filepath):
        print(f"Fixed: {filepath}")
    else:
        print(f"Skipped (already fixed): {filepath}")
