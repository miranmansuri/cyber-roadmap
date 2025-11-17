#!/usr/bin/env python3
import socket
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def grab_banner(target, port=80, timeout=5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((target, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore')
        s.close()
        return banner.strip()
    except Exception as e:
        return f"{Fore.RED}ERROR: {e}{Style.RESET_ALL}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Usage: python3 banner_grabber.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    target = sys.argv[1]
    print(f"{Fore.CYAN}[*] Grabbing banner from {target}:80{Style.RESET_ALL}")
    banner = grab_banner(target)
    print(f"{Fore.GREEN}[+] Banner:\n{banner}{Style.RESET_ALL}")
