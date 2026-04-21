import subprocess
import shutil


def run_nmap_scan(target="127.0.0.1"):
    if not shutil.which("nmap"):
        return "[Pentabot] Nmap not installed"

    return subprocess.getoutput(f"nmap -sV {target}")