#!/usr/bin/env python3
import subprocess
from colorama import init, Fore, Style
init(autoreset=True)

print(f"{Fore.CYAN}=== MIRAN'S MULTI-IP SCANNER v2 ==={Style.RESET_ALL}\n")

ips = ["8.8.8.8", "1.1.1.1", "1.0.0.1", "google.com", "192.168.1.999"]
alive_count = 0

for ip in ips:
    result = subprocess.run(
        ['ping', '-c', '1', '-W', '1', ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    if result.returncode == 0:
        print(f"{Fore.GREEN}[+] {ip:<20} → ALIVE AND READY TO ATTACK")
        alive_count += 1
    else:
        print(f"{Fore.RED}[-] {ip:<20} → dead or firewalled")

print(f"\n{Fore.YELLOW}Scan complete: {alive_count}/{len(ips)} targets alive.{Style.RESET_ALL}")
