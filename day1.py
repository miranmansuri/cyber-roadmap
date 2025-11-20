#!/usr/bin/env python3
print("=== PYTHON ZERO TO HERO – DAY 1 ===")
name = input("What is your hacker name? ")
print(f"Welcome, {name}! You are now leaving the matrix.")
tools = ["nmap", "metasploit", "burp", "john", "hydra", "sqlmap", "wireshark"]
print(f"\nYou will master {len(tools)} tools in 90 days:")
for tool in tools:
    print(f"→ {tool.upper()}")
if name.lower() == "neo":
    print("\nThere is no spoon.")
else:
    print(f"\n{name}, you have 90 days to become unstoppable.")

