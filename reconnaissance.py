__tool__ = "Reconnaissance"
__version__ = "1.1.4"
__author__ = "cinar59101"

# -*- coding: utf-8 -*-
import requests
from colorama import Fore, init
import sys
import time
import argparse

init(autoreset=True)

# ===================== CONFIG =====================
GITHUB_REPO = "cinar59101/Reconnaissance"

SCAN_MODE = "fast"
REQUEST_TIMEOUT = 8

HEADERS = {
    "User-Agent": f"Reconnaissance-OSINT/{__version__}"
}

# ===================== SITE GROUPS =====================
SITE_GROUPS = {
    "social": {
        "Instagram": ("https://www.instagram.com/{}/", "sorry"),
        "Twitter / X": ("https://x.com/{}", "doesn’t exist"),
        "TikTok": ("https://www.tiktok.com/@{}", "couldn't find"),
        "Reddit": ("https://www.reddit.com/user/{}", "nobody"),
        "Pinterest": ("https://www.pinterest.com/{}/", "404"),
        "Tumblr": ("https://{}.tumblr.com", "not found"),
    },
    "dev": {
        "GitHub": ("https://github.com/{}", "not found"),
        "GitLab": ("https://gitlab.com/{}", "not found"),
        "Bitbucket": ("https://bitbucket.org/{}", "not found"),
        "StackOverflow": ("https://stackoverflow.com/users/{}", "page not found"),
        "Kaggle": ("https://www.kaggle.com/{}", "404"),
    },
    "gaming": {
        "Steam": ("https://steamcommunity.com/id/{}", "could not be found"),
        "Roblox": ("https://www.roblox.com/user.aspx?username={}", "page cannot be found"),
        "NameMC": ("https://namemc.com/profile/{}", "not found"),
    },
    "content": {
        "YouTube": ("https://www.youtube.com/@{}", "404"),
        "Twitch": ("https://www.twitch.tv/{}", "sorry"),
        "SoundCloud": ("https://soundcloud.com/{}", "404"),
        "Medium": ("https://medium.com/@{}", "404"),
        "DeviantArt": ("https://www.deviantart.com/{}", "deviantart"),
        "Patreon": ("https://www.patreon.com/{}", "not found"),
    }
}

# ===================== ARGUMENTS =====================
def parse_args():
    parser = argparse.ArgumentParser(
        description="Reconnaissance OSINT CLI Framework"
    )

    parser.add_argument("-u", "--username", help="Username to scan")
    parser.add_argument("--mode", choices=["fast", "strict"], help="Scan mode")
    parser.add_argument("--only", choices=SITE_GROUPS.keys(), help="Scan only one group")
    parser.add_argument("--timeout", type=int, help="Request timeout (seconds)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    # NEW
    parser.add_argument(
        "--wizard",
        action="store_true",
        help="Launch interactive menu (wizard mode)"
    )

    return parser.parse_args()

# ===================== BANNER =====================
def banner():
    print(Fore.CYAN + f"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝

   Reconnaissance OSINT CLI Framework
        Version {__version__}
        Author  {__author__}
============================================
""")

# ===================== SAFE REQUEST =====================
def safe_request(url):
    try:
        return requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )
    except requests.exceptions.Timeout:
        return "timeout"
    except requests.exceptions.RequestException:
        return "error"

# ===================== SCAN MODE =====================
def select_scan_mode():
    global SCAN_MODE

    while True:
        print("""
Select scan mode:
[1] Fast Scan
[2] Strict Scan
""")
        choice = input("Mode: ").strip()

        if choice == "1":
            SCAN_MODE = "fast"
            break
        elif choice == "2":
            SCAN_MODE = "strict"
            break
        else:
            print("[!] Invalid mode, try again.")

    print(f"[✓] Scan mode set to: {SCAN_MODE.upper()}")

# ===================== UPDATE CHECK =====================
def check_for_updates():
    print(Fore.BLUE + "\n[*] Checking for updates...\n")
    print(Fore.YELLOW + "GitHub Actions auto-update is enabled.\n")

# ===================== USERNAME OSINT =====================
def username_osint(username, group=None):
    print(Fore.CYAN + f"\n[+] Target: {username}")
    print(Fore.MAGENTA + f"[i] Mode: {SCAN_MODE.upper()}\n")

    sites = SITE_GROUPS[group] if group else {
        k: v for grp in SITE_GROUPS.values() for k, v in grp.items()
    }

    found = not_found = timeout = 0

    for site, data in sites.items():
        url_template, proof = data
        url = url_template.format(username)

        print(Fore.BLUE + f"[*] Checking {site}...")
        time.sleep(0.25)

        r = safe_request(url)

        if r == "timeout":
            print(Fore.YELLOW + f"[TIMEOUT] {site}")
            timeout += 1
            continue

        if r == "error":
            print(Fore.MAGENTA + f"[ERROR] {site}")
            continue

        page = r.text.lower()

        if SCAN_MODE == "fast":
            if r.status_code == 200:
                print(Fore.GREEN + f"[FOUND] {site}: {url}")
                found += 1
            else:
                print(Fore.RED + f"[NOT FOUND] {site}")
                not_found += 1
        else:
            if r.status_code == 200 and proof.lower() not in page:
                print(Fore.GREEN + f"[FOUND] {site}: {url}")
                found += 1
            else:
                print(Fore.RED + f"[NOT FOUND] {site}")
                not_found += 1

    print(Fore.CYAN + "\n========== SUMMARY ==========")
    print(Fore.GREEN + f"✔ Found     : {found}")
    print(Fore.RED + f"✖ Not Found : {not_found}")
    print(Fore.YELLOW + f"⏱ Timeout   : {timeout}")
    print(Fore.CYAN + "=============================\n")

# ===================== MENU (WIZARD) =====================
def menu():
    while True:
        print(Fore.YELLOW + """
[1] Username Reconnaissance
[2] Change Scan Mode
[3] Check for updates
[0] Exit
""")
        choice = input(Fore.CYAN + "Select option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            if username:
                username_osint(username)
        elif choice == "2":
            select_scan_mode()
        elif choice == "3":
            check_for_updates()
        elif choice == "0":
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid selection.")

# ===================== MAIN =====================
if __name__ == "__main__":
    args = parse_args()

    if args.no_color:
        init(strip=True)

    if args.timeout:
        REQUEST_TIMEOUT = args.timeout

    if args.mode:
        SCAN_MODE = args.mode

    banner()

    # WIZARD MODE
    if args.wizard:
        menu()
        sys.exit(0)

    # PARAMETER ENFORCEMENT
    if not args.username:
        print(Fore.RED + "[!] Username is required unless --wizard is used.\n")
        print("Examples:")
        print("  python reconnaissance.py -u username")
        print("  python reconnaissance.py -u username --only social")
        print("  python reconnaissance.py --wizard\n")
        sys.exit(1)

    # CLI MODE
    username_osint(args.username, args.only)
