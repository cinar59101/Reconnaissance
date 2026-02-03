__tool__ = "Reconnaissance"
__version__ = "1.1.1"
__author__ = "cinar59101"

# -*- coding: utf-8 -*-
import requests
from colorama import Fore, init
import sys
import time
import os

init(autoreset=True)

GITHUB_REPO = "cinar59101/Reconnaissance"
RAW_FILE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/reconnaissance.py"

HEADERS = {
    "User-Agent": f"Reconnaissance-OSINT/{__version__}"
}

# ===================== BANNER =====================
def banner():
    print(Fore.CYAN + f"""
====================================
        Reconnaissance
     OSINT CLI Framework
        v{__version__}
====================================
""")

# ===================== MENU =====================
def menu():
    while True:
        print(Fore.YELLOW + """
[1] Username Reconnaissance
[2] Check for updates
[0] Exit
""")
        try:
            choice = input(Fore.CYAN + "Select option: ").strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nExiting...")
            sys.exit(0)

        if choice == "1":
            username = input("Username: ").strip()
            if username:
                username_osint(username)
            else:
                print(Fore.RED + "Username cannot be empty.")

        elif choice == "2":
            check_for_updates()

        elif choice == "0":
            print(Fore.GREEN + "Goodbye.")
            break

        else:
            print(Fore.RED + "Invalid selection.")

# ===================== SAFE REQUEST =====================
def safe_request(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=8)
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.RequestException:
        return "error"

# ===================== VERSION UTILS =====================
def version_tuple(v):
    return tuple(map(int, v.split(".")))

# ===================== UPDATE SYSTEM =====================
def check_for_updates():
    print(Fore.BLUE + "\n[*] Checking for updates...\n")

    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

    try:
        r = requests.get(api_url, timeout=8)
        if r.status_code != 200:
            print(Fore.RED + "[!] Could not reach GitHub.")
            return

        latest_version = r.json()["tag_name"].lstrip("v")

        if version_tuple(latest_version) > version_tuple(__version__):
            print(Fore.GREEN + f"[+] New version available: v{latest_version}")
            choice = input(Fore.CYAN + "[?] Update now? (y/n): ").lower().strip()

            if choice == "y":
                download_and_update()
            else:
                print(Fore.YELLOW + "Update skipped.")
        else:
            print(Fore.GREEN + "[✓] You are using the latest version.")

    except Exception as e:
        print(Fore.RED + f"[ERROR] Update check failed: {e}")

def download_and_update():
    current_file = os.path.realpath(__file__)
    backup_file = current_file + ".bak"

    try:
        print(Fore.BLUE + "[*] Downloading latest version...")

        r = requests.get(RAW_FILE_URL, timeout=15)
        if r.status_code != 200:
            print(Fore.RED + "[!] Failed to download update.")
            return

        # Backup
        if os.path.exists(backup_file):
            os.remove(backup_file)
        os.rename(current_file, backup_file)

        with open(current_file, "w", encoding="utf-8") as f:
            f.write(r.text)

        print(Fore.GREEN + "[+] Update successful!")
        print(Fore.YELLOW + "[!] Restart the tool to apply the update.")
        sys.exit(0)

    except Exception as e:
        print(Fore.RED + f"[!] Update failed: {e}")
        if os.path.exists(backup_file):
            os.rename(backup_file, current_file)
            print(Fore.YELLOW + "[!] Previous version restored.")

# ===================== USERNAME OSINT =====================
def username_osint(username):
    print(Fore.CYAN + f"\n[+] Starting username reconnaissance: {username}\n")

    sites = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter / X": f"https://x.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
    }

    for site, url in sites.items():
        print(Fore.BLUE + f"[*] Checking {site}...")
        time.sleep(0.4)

        r = safe_request(url)

        if r == "timeout":
            print(Fore.YELLOW + f"[TIMEOUT] {site}")
        elif r == "error":
            print(Fore.MAGENTA + f"[ERROR] {site}")
        elif r.status_code == 200:
            print(Fore.GREEN + f"[FOUND] {site}: {url}")
        else:
            print(Fore.RED + f"[NOT FOUND] {site}")

# ===================== MAIN =====================
if __name__ == "__main__":
    banner()
    menu()
