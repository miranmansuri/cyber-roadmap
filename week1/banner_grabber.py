#!/usr/bin/env python3
import socket
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def grab_banner(target, port, timeout=5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((target, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n") if port in [80, 443] else s.send(b"\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner if banner else "No banner"
    except Exception as e:
        return f"{Fore.RED}Closed/Filtered{Style.RESET_ALL}"

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Usage: python3 banner_grabber.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    target = sys.argv[1]
    ports = [21, 22, 25, 80, 443, 8080]
    results = []

    print(f"{Fore.CYAN}[*] Starting multi-port banner grab on {target}{Style.RESET_ALL}\n")
    
    for port in ports:
        print(f"{Fore.MAGENTA}[→] Checking port {port:5} ...", end="")
        banner = grab_banner(target, port)
        status = f"{Fore.GREEN}OPEN" if "Closed" not in banner else f"{Fore.RED}CLOSED"
        print(f" {status}{Style.RESET_ALL}")
        if "Closed" not in banner and banner != "No banner":
            print(f"    └─ {Fore.YELLOW}{banner.replace(chr(10), chr(10)+'       ')}{Style.RESET_ALL}")
        results.append(f"Port {port}: {status} → {banner}")

    # Save report
    with open("scan_report.txt", "w") as f:
        f.write(f"Target: {target}\n")
        f.write(f"Scan time: {__import__('datetime').datetime.now()}\n\n")
        f.write("\n".join(results))
    
    print(f"\n{Fore.CYAN}[+] Report saved → scan_report.txt{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
