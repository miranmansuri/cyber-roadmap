#!/usr/bin/env python3
import subprocess
import sys
from colorama import init, Fore

init(autoreset=True)

def ping_host(host):
    result = subprocess.run(['ping', '-c', '1', '-W', '1', host],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

if __name__ == "__main__":
    print(f"{Fore.YELLOW}=== HOST CHECKER v2 ==={Fore.RESET}")
    hosts = input(f"{Fore.CYAN}Enter IPs (space-separated): {Fore.RESET}").strip().split()
    
    if not hosts:
        print(f"{Fore.RED}No hosts entered!{Fore.RESET}")
        sys.exit(1)
    
    for host in hosts:
        status = f"{Fore.GREEN}UP" if ping_host(host) else f"{Fore.RED}DOWN"
        print(f"{Fore.CYAN}{host}{Fore.RESET} is {status}{Fore.RESET}")
