#!/usr/bin/env python3
import subprocess
import socket
import sys
import os
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def ping_host(ip):
    result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def grab_banner(ip, port, timeout=3):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n") if port in [80, 443] else s.send(b"\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner if banner else "No banner"
    except:
        return None

def run_dirb(target):
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if not os.path.exists(wordlist):
        print(f"{Fore.RED}[!] dirb wordlist missing!{Style.RESET_ALL}")
        return []
    result = subprocess.run(['dirb', f"http://{target}", wordlist, '-S'],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lines = [l for l in result.stdout.split('\n') if '+' in l and 'CODE:200' in l or 'CODE:301' in l]
    return lines[:10]  # top 10 findings

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Usage: python3 recon.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    target = sys.argv[1]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_file = f"recon_report_{target}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    
    print(f"{Fore.CYAN}[*] Starting full recon on {target} @ {timestamp}{Style.RESET_ALL}\n")
    
    # 1. Host check
    print(f"{Fore.MAGENTA}[1] Host discovery...", end="")
    alive = ping_host(target)
    status = f"{Fore.GREEN}UP" if alive else f"{Fore.RED}DOWN"
    print(f" {status}{Style.RESET_ALL}")
    if not alive:
        print(f"{Fore.RED}Target down → exiting{Style.RESET_ALL}")
        sys.exit(0)
    
    # 2. Banner grab
    ports = [21, 22, 25, 80, 443, 8080]
    open_ports = []
    banners = []
    print(f"{Fore.MAGENTA}[2] Banner grabbing...")
    for port in ports:
        print(f"    └─ Port {port:5} → ", end="")
        banner = grab_banner(target, port)
        if banner:
            open_ports.append(port)
            banners.append(f"Port {port} → {banner}")
            print(f"{Fore.GREEN}OPEN → {banner.split(chr(10))[0]}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}CLOSED{Style.RESET_ALL}")
    
    # 3. Dirb
    print(f"\n{Fore.MAGENTA}[3] Directory enumeration (top 10)...")
    findings = run_dirb(target)
    for f in findings:
        print(f"    └─ {Fore.YELLOW}{f}{Style.RESET_ALL}")
    
    # 4. Save HTML report
    with open(report_file, "w") as f:
        f.write(f"<h1>Recon Report - {target}</h1><h3>{timestamp}</h3><pre>")
        f.write(f"Host: <b>{status}</b>\n\n")
        f.write("Open ports & banners:\n" + "\n".join(banners) + "\n\n")
        f.write("Directory findings:\n" + "\n".join(findings))
        f.write("</pre>")
    
    print(f"\n{Fore.CYAN}[+] Full HTML report saved → {report_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
