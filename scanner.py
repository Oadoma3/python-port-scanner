import sys
import socket

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
    443, 445, 587, 993, 995, 1433, 1521, 2049, 3306,
    3389, 5432, 5900, 6379, 8080
]

def scan_port(host: str, port: int, timeout: float = 0.8) -> bool:
    """Return True if TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except OSError:
        return False

def grab_banner(host: str, port: int, timeout: float = 1.0) -> str:
    """Attempt to read a banner from an open port (best-effort)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            # Many services won't send anything unless you speak protocol,
            # but some do (or respond to a newline).
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
    if len(sys.argv) < 2:
        print("Usage: python scanner.py <host> [--banner]")
        sys.exit(1)

    host = sys.argv[1]
    do_banner = "--banner" in sys.argv[2:]

    # Resolve host early so failures are clear
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Error: could not resolve host: {host}")
        sys.exit(1)

    print("\n=== Python Port Scanner ===")
    print(f"Target: {host} ({ip})")
    print(f"Ports: {len(COMMON_PORTS)} common ports")
    print(f"Banner grabbing: {'ON' if do_banner else 'OFF'}\n")

    open_ports = []
    for port in COMMON_PORTS:
        if scan_port(ip, port):
            open_ports.append(port)
            if do_banner:
                banner = grab_banner(ip, port)
                print(f"[OPEN] {port:>5}  {banner}")
            else:
                print(f"[OPEN] {port:>5}")

    print("\nSummary:")
    if not open_ports:
        print("- No open ports found in the common-port list.")
    else:
        print(f"- Open ports: {', '.join(map(str, open_ports))}")

if __name__ == "__main__":
    main()
