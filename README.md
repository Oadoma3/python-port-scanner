# Python Port Scanner

## Description

A Python TCP port scanner that checks a target host for open ports and optionally grabs service banners. Built to practice networking, security scripting, and clean CLI-style tooling.

## Features

- Scans a target host for open TCP ports
- Supports a default common-port list (25 well-known ports)
- Custom port ranges or lists with `-p` (e.g. `1-1024` or `80,443,8080`)
- Optional banner grabbing for detected services (`--banner`)
- Configurable connection timeout (`--timeout`)
- Save results to a file (`--output`)

## Tech

- Python 3
- Sockets (standard library)
- Argparse (standard library)
- Git/GitHub

## Installation

No dependencies required — uses Python standard library only.

```bash
git clone https://github.com/Oadoma3/python-port-scanner.git
cd python-port-scanner
```

## Usage

```bash
python scanner.py <host> [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--banner` | Attempt to grab service banners from open ports |
| `-p`, `--ports` | Port range or list (e.g. `1-1024` or `80,443,8080`). Defaults to common ports |
| `--timeout` | Connection timeout in seconds per port (default: 0.8) |
| `--output` | Save results to a file (e.g. `results.txt`) |

## Examples

```bash
# Scan common ports
python scanner.py example.com

# Scan with banner grabbing
python scanner.py example.com --banner

# Scan a custom port range
python scanner.py example.com -p 1-1024

# Scan specific ports
python scanner.py example.com -p 80,443,8080

# Save results to a file
python scanner.py example.com --output results.txt

# Full example — custom range, banners, custom timeout, save output
python scanner.py example.com -p 1-1024 --banner --timeout 1.5 --output results.txt
```

## Example Output

```
=== Python Port Scanner ===
Target : example.com (93.184.216.34)
Ports  : 25 ports
Banner : ON
Timeout: 0.8s

[OPEN]    80  (no banner)
[OPEN]   443  (no banner)

Summary:
  Open ports: 80, 443
```
