#!/usr/bin/env python3
"""
Script to replace telebot.types with types and add proper imports
"""
import os
import re
from pathlib import Path


def fix_telebot_imports(file_path):
    """Fix telebot.types imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Check if file uses telebot.types
        if 'telebot.types' not in content:
            return False

        # Add import if not present
        if 'from telebot import types' not in content and 'import telebot' in content:
            # Find the import telebot line and add types import after it
            content = re.sub(r'(import telebot.*?\n)', r'\1from telebot import types\n', content, count=1)

        # Replace all telebot.types with types
        content = re.sub(r'telebot\.types\.', 'types.', content)

        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed: {file_path}')
            return True

        return False
    except Exception as e:
        print(f'Error processing {file_path}: {e}')
        return False


def main():
    """Main function to process all Python files"""
    base_dir = Path('.')
    target_dirs = ['api', 'botApp', 'botCast', 'botCommands', 'botCore', 'botRoutes', 'core', 'db', 'flaskApp', 'tests']

    fixed_count = 0

    for dir_name in target_dirs:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            print(f'Directory not found: {dir_name}')
            continue

        # Find all Python files recursively
        for py_file in dir_path.rglob('*.py'):
            if fix_telebot_imports(py_file):
                fixed_count += 1

    print(f'\nFixed {fixed_count} files')


if __name__ == '__main__':
    main()
