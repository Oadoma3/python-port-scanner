
# Python Port Scanner

## Description
A simple Python port scanner that checks common TCP ports on a target host and optionally grabs service banners. Built to practice networking, security scripting, and clean CLI-style tooling.

## Features
- Scans a target host for open TCP ports
- Supports scanning a default common-port list
- Optional banner grabbing for detected services
- Prints a clear results summary (terminal)

## Tech
- Python 3
- Sockets (standard library)
- Git/GitHub

## How to Run
1. Clone the repo
2. Run a scan:
   ```bash
   python scanner.py example.com
   python scanner.py example.com --banner

