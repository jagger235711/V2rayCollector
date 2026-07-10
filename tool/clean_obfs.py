#!/usr/bin/env python3
"""Remove obfs field from proxies that have obfs but no obfs-password.

Usage: python3 clean_obfs.py <input_yaml> [output_yaml]
If output_yaml is omitted, the input file is modified in place.
"""

import sys
import yaml


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 clean_obfs.py <input_yaml> [output_yaml]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    with open(input_path) as f:
        data = yaml.safe_load(f)

    if 'proxies' not in data:
        print("No 'proxies' field found, nothing to clean")
        return

    fixed = 0
    for p in data['proxies']:
        # mihomo requires: if obfs is set and non-empty, obfs-password MUST be non-empty too.
        # If the proxy has obfs but no obfs-password, the safest fix is to
        # clear obfs entirely (disable obfs) rather than guessing a password.
        if p.get('obfs') and not p.get('obfs-password'):
            p['obfs'] = ''
            fixed += 1

    with open(output_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

    print(f"Fixed {fixed} proxies: cleared obfs (no password), "
          f"total {len(data['proxies'])} proxies")


if __name__ == '__main__':
    main()
