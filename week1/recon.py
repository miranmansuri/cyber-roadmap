#!/usr/bin/env python3
import subprocess
import socket
import sys
import os
import xml.etree.ElementTree as ET
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

def ping_host(ip):
    return subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def run_nmap(target):
    xml_file = f"nmap_{target}.xml"
    print(f"{Fore.MAGENTA}[3] Running Nmap version scan → {xml_file}{Style.RESET_ALL}")
    subprocess.run(['nmap', '-sV', '-oX', xml_file, target], check=True)
    return xml_file

def parse_nmap_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    vulns = []
    for port in root.findall('.//port'):
        state = port.find('state').get('state')
        if state != 'open': continue
        service = port.find('service')
        if service is None: continue
        name = service.get('name', 'unknown')
        product = service.get('product', '')
        version = service.get('version', '')
        banner = f"{product} {version}".strip()
        portid = port.get('portid')
        
        # Simple CVE hints
        cve = ""
        if "OpenSSH 6.6" in banner:
            cve = "CVE-2016-0777, CVE-2016-0778 (info leak)"
        elif "Apache 2.4.7" in banner:
            cve = "CVE-2014-0226, CVE-2014-0231 (DoS)"
        
        vulns.append(f"Port {portid} → {name.upper()} → {banner} → {Fore.RED}{cve}{Style.RESET_ALL}" if cve else f"Port {portid} → {name.upper()} → {banner}")
    return vulns

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Usage: python3 recon.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    target = sys.argv[1]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"FINAL_REPORT_{target}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    
    print(f"{Fore.CYAN}[*] ULTIMATE RECON v2 → {target} @ {timestamp}{Style.RESET_ALL}\n")
    
    # 1. Host alive?
    print(f"{Fore.MAGENTA}[1] Host discovery...", "UP" if ping_host(target) else "DOWN")
    if not ping_host(target):
        sys.exit(0)
    
    # 2. Nmap + parse
    xml = run_nmap(target)
    findings = parse_nmap_xml(xml)
    
    # 3. Save epic report
    with open(report, "w") as f:
        f.write(f"<h1>ULTIMATE RECON REPORT – {target}</h1><h2>{timestamp}</h2><pre>")
        f.write("\n".join(findings))
        f.write("</pre>")
    
    print(f"\n{Fore.CYAN}[+] FINAL REPORT → {report}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}    Open with: firefox {report}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
