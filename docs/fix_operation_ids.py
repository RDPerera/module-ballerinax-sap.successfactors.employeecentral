#!/usr/bin/env python3
"""
Script to add missing operationId fields to OpenAPI specifications.
This fixes the client generation failures caused by missing operation IDs.
"""

import json
import re
from pathlib import Path

def generate_operation_id(method, path, summary=None):
    """Generate operation ID based on HTTP method, path, and summary."""
    # Clean the path - remove parameters and special characters
    clean_path = re.sub(r'\([^)]*\)', '', path)
    clean_path = re.sub(r'[{}()]', '', clean_path)
    clean_path = re.sub(r'[/\-_]+', '_', clean_path).strip('_')
    
    # Convert to camelCase
    parts = clean_path.split('_')
    if parts and parts[0]:
        camel_case = parts[0].lower()
        for part in parts[1:]:
            if part:
                camel_case += part.capitalize()
    else:
        camel_case = "operation"
    
    # Add method prefix
    method_prefixes = {
        'get': 'get' if '(' in path else 'list',
        'post': 'create',
        'put': 'update',
        'delete': 'delete',
        'patch': 'patch'
    }
    
    prefix = method_prefixes.get(method.lower(), method.lower())
    
    if prefix == 'list':
        # For collection operations, use plural form
        operation_id = f"{prefix}{camel_case}s" if camel_case and not camel_case.endswith('s') else f"{prefix}{camel_case}"
    elif prefix == 'get':
        # For single entity operations
        operation_id = f"{prefix}{camel_case}"
    else:
        # For create, update, delete
        operation_id = f"{prefix}{camel_case}"
    
    return operation_id

def add_operation_ids(spec_file):
    """Add operation IDs to all operations in the OpenAPI spec."""
    print(f"Processing {spec_file}...")
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    paths = spec.get('paths', {})
    modified = False
    
    for path, path_obj in paths.items():
        for method, operation in path_obj.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch'] and isinstance(operation, dict):
                if 'operationId' not in operation:
                    summary = operation.get('summary', '')
                    operation_id = generate_operation_id(method, path, summary)
                    operation['operationId'] = operation_id
                    modified = True
                    print(f"  Added operationId '{operation_id}' for {method.upper()} {path}")
    
    if modified:
        # Write back to file with proper formatting
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2, separators=(',', ':'), ensure_ascii=False)
        print(f"✅ Updated {spec_file}")
    else:
        print(f"ℹ️  No changes needed for {spec_file}")

def main():
    """Main function to process all failing API specs."""
    failing_apis = [
        'ECApprenticeManagement.json',
        'ECCompensationInformation.json',
        'ECDismissalProtection.json',
        'ECEmploymentInformation.json'
    ]
    
    spec_dir = Path('spec')
    
    for api_file in failing_apis:
        spec_path = spec_dir / api_file
        if spec_path.exists():
            add_operation_ids(spec_path)
        else:
            print(f"❌ File not found: {spec_path}")
    
    print("\n🎉 Operation ID fixing completed!")

if __name__ == '__main__':
    main()
