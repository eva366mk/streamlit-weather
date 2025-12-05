#!/usr/bin/env python3
"""Prompt for OPENWEATHER_API_KEY and write a .env file in the project root.
Usage: python write_env.py
This avoids storing the key in source files or the shell history.
"""
import getpass
from pathlib import Path

def main():
    key = getpass.getpass('Enter OPENWEATHER_API_KEY (input hidden): ')
    if not key:
        print('No key entered. Aborting.')
        return
    env_path = Path('.') / '.env'
    if env_path.exists():
        confirm = input('.env already exists. Overwrite? (y/N): ').strip().lower()
        if confirm != 'y':
            print('.env not changed.')
            return
    env_path.write_text(f'OPENWEATHER_API_KEY={key}', encoding='utf-8')
    print(f'.env created at {env_path.resolve()}')
    print('Note: .env is in .gitignore; do not commit it to git')

if __name__ == '__main__':
    main()
