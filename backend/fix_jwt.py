"""
Fix all get_jwt_identity() calls to convert to int
"""
import re
import os

# Files to fix
files = [
    'app/routes/auth.py',
    'app/routes/products.py',
    'app/routes/inventory.py',
    'app/routes/sales.py',
    'app/routes/excel_import_export.py',
    'app/routes/settings.py',
    'app/routes/payroll.py'
]

base_dir = r'D:\Management Processes Systems\backend'

for file_path in files:
    full_path = os.path.join(base_dir, file_path)
    
    if not os.path.exists(full_path):
        print(f"Skipping {file_path} - file not found")
        continue
    
    print(f"\nProcessing {file_path}...")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count current instances
    current_count = content.count('get_jwt_identity()')
    already_fixed = content.count('int(get_jwt_identity())')
    
    print(f"  Found {current_count} instances")
    print(f"  Already fixed: {already_fixed}")
    
    # Replace all instances of `user_id = get_jwt_identity()` with `user_id = int(get_jwt_identity())`
    # But don't double-fix ones that are already int()
    pattern = r'(\s+)(user_id|current_user_id) = get_jwt_identity\(\)'
    replacement = r'\1\2 = int(get_jwt_identity())'
    
    new_content = re.sub(pattern, replacement, content)
    
    # Count new instances
    new_already_fixed = new_content.count('int(get_jwt_identity())')
    
    if new_content != content:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Fixed {new_already_fixed - already_fixed} instances")
    else:
        print(f"  No changes needed")

print("\n✓ All files processed!")
