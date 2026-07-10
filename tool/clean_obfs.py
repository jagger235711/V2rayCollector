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
        # Only hysteria2 requires obfs-password when obfs is set.
        # Other protocols (SSR, VMess) use obfs differently without needing obfs-password.
        if p.get('type') == 'hysteria2' and p.get('obfs') and not p.get('obfs-password'):
            p['obfs'] = ''
            fixed += 1

    with open(output_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

    print(f"Fixed {fixed} hysteria2 proxies: cleared obfs (no password), "
          f"total {len(data['proxies'])} proxies")


if __name__ == '__main__':
    main()
