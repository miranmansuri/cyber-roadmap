#!/usr/bin/env python3
import subprocess
import sys

# Force color even in some terminals
import os
os.system('')  # Enables ANSI in Windows, harmless in Linux
from colorama import init, Fore
init(autoreset=True)  # Auto-reset colors
