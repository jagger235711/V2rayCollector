#!/usr/bin/env python3
"""Validate and clean proxy configurations before running clash-speedtest.

Removes proxies with invalid or missing required fields that would cause
mihomo/clash-speedtest to fail on load.

Usage: python3 clean_proxies.py <input_yaml> [output_yaml]
If output_yaml is omitted, the input file is modified in place.
"""

import sys
import yaml

# Valid Shadowsocks ciphers (mihomo supported list)
VALID_SS_CIPHERS = {
    "aes-128-gcm", "aes-192-gcm", "aes-256-gcm",
    "aes-128-ctr", "aes-192-ctr", "aes-256-ctr",
    "aes-128-cfb", "aes-192-cfb", "aes-256-cfb",
    "rc4-md5", "chacha20-ietf-poly1305", "xchacha20-ietf-poly1305",
    "none", "plain",
}

# Proxy types that we know how to validate
PROXY_TYPES_WITH_CIPHER = {"ss", "shadowsocks"}


def is_valid_proxy(p):
    """Check if a proxy has valid required fields."""
    ptype = p.get('type', '')
    name = p.get('name', 'unnamed')

    # Every proxy needs a type
    if not ptype:
        print(f"  Removing {name}: missing type")
        return False

    # Shadowsocks: cipher must be valid
    if ptype in PROXY_TYPES_WITH_CIPHER:
        cipher = p.get('cipher', '')
        if not cipher or cipher not in VALID_SS_CIPHERS:
            print(f"  Removing {name}: invalid ss cipher '{cipher}'")
            return False

    # Every proxy needs server and port
    if not p.get('server'):
        print(f"  Removing {name}: missing server")
        return False
    if not isinstance(p.get('port'), int) or p.get('port') <= 0:
        print(f"  Removing {name}: invalid port")
        return False

    return True


def fix_hysteria2_obfs(p):
    """Fix hysteria2 proxies that have obfs set but no obfs-password."""
    if p.get('type') == 'hysteria2' and p.get('obfs') and not p.get('obfs-password'):
        p['obfs'] = ''
        return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 clean_proxies.py <input_yaml> [output_yaml]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    with open(input_path) as f:
        data = yaml.safe_load(f)

    if 'proxies' not in data or not data['proxies']:
        print("No proxies found, nothing to clean")
        return

    proxies = data['proxies']
    total = len(proxies)

    # Fix phase: repair proxies where possible
    fixes = 0
    for p in proxies:
        if fix_hysteria2_obfs(p):
            fixes += 1

    # Filter phase: remove proxies that can't be fixed
    valid = [p for p in proxies if is_valid_proxy(p)]
    removed = total - len(valid)
    data['proxies'] = valid

    with open(output_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

    print(f"Fixed {fixes} hysteria2 obfs, removed {removed} invalid proxies, "
          f"{len(valid)}/{total} proxies remaining")


if __name__ == '__main__':
    main()
