import sys
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
    443, 445, 587, 993, 995, 1433, 1521, 2049, 3306,
    3389, 5432, 5900, 6379, 8080
]


def parse_port_range(port_arg: str) -> list[int]:
    ports = []
    for part in port_arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))


def scan_port(host: str, port: int, timeout: float = 0.8) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except OSError:
        return False


def grab_banner(host: str, port: int, timeout: float = 1.0) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            try:
                s.sendall(b"\r\n")
            except OSError:
                pass
            data = s.recv(1024)
            banner = data.decode(errors="ignore").strip()
            return banner if banner else "(no banner)"
    except OSError:
        return "(banner grab failed)"


def main():
    parser = argparse.ArgumentParser(
        prog="scanner.py",
        description="A simple TCP port scanner with optional banner grabbing.",
    )
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("--banner", action="store_true", help="Attempt to grab service banners from open ports")
    parser.add_argument("-p", "--ports", help="Port range or list (e.g. 1-1024 or 80,443,8080). Defaults to common ports.", default=None)
    parser.add_argument("--timeout", type=float, default=0.8, help="Connection timeout in seconds per port (default: 0.8)")
    parser.add_argument("--output", help="Save results to a file (e.g. results.txt)", default=None)
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads (default: 100)")
    args = parser.parse_args()

    ports = parse_port_range(args.ports) if args.ports else COMMON_PORTS

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Error: could not resolve host: {args.host}")
        sys.exit(1)

    lines = []
    lines.append("\n=== Python Port Scanner ===")
    lines.append(f"Target  : {args.host} ({ip})")
    lines.append(f"Ports   : {len(ports)} ports")
    lines.append(f"Threads : {args.threads}")
    lines.append(f"Banner  : {'ON' if args.banner else 'OFF'}")
    lines.append(f"Timeout : {args.timeout}s\n")

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, ip, port, args.timeout): port for port in ports}
        for future in as_completed(futures):
            port = futures[future]
            if future.result():
                open_ports.append(port)

    open_ports.sort()

    for port in open_ports:
        if args.banner:
            banner = grab_banner(ip, port)
            lines.append(f"[OPEN] {port:>5}  {banner}")
        else:
            lines.append(f"[OPEN] {port:>5}")

    lines.append("\nSummary:")
    if not open_ports:
        lines.append("  No open ports found.")
    else:
        lines.append(f"  Open ports: {', '.join(map(str, open_ports))}")

    output = "\n".join(lines)
    print(output)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()