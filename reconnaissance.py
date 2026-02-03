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
            check_for_update()

        elif choice == "0":
            print(Fore.GREEN + "Goodbye.")
            break

        else:
            print(Fore.RED + "Invalid selection.")

# ===================== SAFE REQUEST =====================
def safe_request(url):
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=8,
            allow_redirects=True
        )
        return r
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.RequestException:
        return "error"

# ===================== UPDATE SYSTEM =====================
def check_for_update():
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

    try:
        r = requests.get(api_url, timeout=6)
        data = r.json()

        latest_version = data["tag_name"].replace("v", "")

        if latest_version != __version__:
            print(Fore.YELLOW + f"\n[+] New version available: v{latest_version}")
            choice = input(Fore.CYAN + "[?] Do you want to update? (y/n): ").lower()

            if choice == "y":
                download_and_update()
            else:
                print(Fore.YELLOW + "Update skipped.")
        else:
            print(Fore.GREEN + "[+] You are using the latest version.")

    except Exception:
        print(Fore.RED + "[!] Failed to check for updates.")

def download_and_update():
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/reconnaissance.py"
    current_file = os.path.realpath(__file__)
    backup_file = current_file + ".bak"

    try:
        print(Fore.BLUE + "[*] Downloading update...")

        r = requests.get(raw_url, timeout=10)

        if r.status_code != 200:
            print(Fore.RED + "[!] Failed to download update.")
            return

        # Backup current file
        os.rename(current_file, backup_file)

        with open(current_file, "w", encoding="utf-8") as f:
            f.write(r.text)

        print(Fore.GREEN + "[+] Update completed successfully.")
        print(Fore.YELLOW + "[!] Restart the tool to apply changes.")
        sys.exit(0)

    except Exception:
        print(Fore.RED + "[!] Update failed. Restoring backup.")
        if os.path.exists(backup_file):
            os.rename(backup_file, current_file)

# ===================== USERNAME OSINT =====================
def username_osint(username):
    print(Fore.CYAN + f"\n[+] Starting username reconnaissance: {username}\n")

    sites = {
        "GitHub": {
            "url": f"https://github.com/{username}",
            "not_found": ["not found"],
            "proof": [f"/{username}", f'>{username}<']
        },
        "Instagram": {
            "url": f"https://www.instagram.com/{username}/",
            "not_found": ["sorry, this page isn't available"],
            "proof": [f'\"username\":\"{username}\"']
        },
        "Twitter / X": {
            "url": f"https://x.com/{username}",
            "not_found": ["this account doesn’t exist", "account suspended"],
            "proof": [f'\"screen_name\":\"{username}\"']
        },
        "TikTok": {
            "url": f"https://www.tiktok.com/@{username}",
            "not_found": ["couldn't find this account"],
            "proof": [f'\"uniqueId\":\"{username}\"']
        },
        "Reddit": {
            "url": f"https://www.reddit.com/user/{username}",
            "not_found": ["page not found", "nobody on reddit"],
            "proof": [f"/user/{username}"]
        }
    }

    for site, data in sites.items():
        print(Fore.BLUE + f"[*] Checking {site}...")
        time.sleep(0.5)

        r = safe_request(data["url"])

        if r == "timeout":
            print(Fore.YELLOW + f"[TIMEOUT] {site}")
            continue
        if r == "error":
            print(Fore.MAGENTA + f"[ERROR] {site}")
            continue

        page = r.text.lower()

        if r.status_code == 404 or any(x in page for x in data["not_found"]):
            print(Fore.RED + f"[NOT FOUND] {site}")
        elif r.status_code == 200 and any(p.lower() in page for p in data["proof"]):
            print(Fore.GREEN + f"[FOUND] {site}: {data['url']}")
        else:
            print(Fore.YELLOW + f"[UNKNOWN] {site}")

# ===================== MAIN =====================
if __name__ == "__main__":
    banner()
    menu()

