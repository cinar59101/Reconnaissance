__tool__ = "Reconnaissance"
__version__ = "1.1.2"
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
        else:
            print(Fore.GREEN + "[✓] You are using the latest version.")

    except Exception as e:
        print(Fore.RED + f"[ERROR] Update check failed: {e}")

# ===================== USERNAME OSINT =====================
def username_osint(username):
    print(Fore.CYAN + f"\n[+] Starting username reconnaissance: {username}\n")

    sites = {
        # DEV / CODE
        "GitHub": "https://github.com/{}",
        "GitLab": "https://gitlab.com/{}",
        "Bitbucket": "https://bitbucket.org/{}",
        "SourceForge": "https://sourceforge.net/u/{}/",

        # SOCIAL
        "Instagram": "https://www.instagram.com/{}/",
        "Twitter / X": "https://x.com/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Pinterest": "https://www.pinterest.com/{}/",
        "Tumblr": "https://{}.tumblr.com",
        "Medium": "https://medium.com/@{}",
        "Quora": "https://www.quora.com/profile/{}",

        # GAMING
        "Steam": "https://steamcommunity.com/id/{}",
        "Roblox": "https://www.roblox.com/user.aspx?username={}",
        "NameMC": "https://namemc.com/profile/{}",

        # MEDIA
        "YouTube": "https://www.youtube.com/@{}",
        "Twitch": "https://www.twitch.tv/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Vimeo": "https://vimeo.com/{}",

        # TECH / SECURITY
        "StackOverflow": "https://stackoverflow.com/users/{}",
        "HackerOne": "https://hackerone.com/{}",
        "TryHackMe": "https://tryhackme.com/p/{}",
        "Keybase": "https://keybase.io/{}",

        # ART / OTHER
        "DeviantArt": "https://www.deviantart.com/{}",
        "Patreon": "https://www.patreon.com/{}",
        "Flickr": "https://www.flickr.com/people/{}/"
    }

    site_checks = {
        "GitHub": ["not found"],
        "GitLab": ["404"],
        "Instagram": ["sorry, this page isn't available"],
        "Twitter / X": ["this account doesn’t exist"],
        "TikTok": ["couldn't find this account"],
        "Reddit": ["nobody on reddit"],
        "Steam": ["the specified profile could not be found"],
        "NameMC": ["profile not found"],
        "YouTube": ["404 not found"],
        "Twitch": ["sorry. unless you’ve got a time machine"],
        "Medium": ["404"],
        "Keybase": ["not found"],
        "TryHackMe": ["page not found"],
    }

    for site, url_template in sites.items():
        url = url_template.format(username)
        print(Fore.BLUE + f"[*] Checking {site}...")
        time.sleep(0.35)

        r = safe_request(url)

        if r == "timeout":
            print(Fore.YELLOW + f"[TIMEOUT] {site}")
            continue

        if r == "error":
            print(Fore.MAGENTA + f"[ERROR] {site}")
            continue

        if r.status_code != 200:
            print(Fore.RED + f"[NOT FOUND] {site}")
            continue

        content = r.text.lower()
        false_hits = site_checks.get(site, [])

        if any(bad in content for bad in false_hits):
            print(Fore.RED + f"[NOT FOUND] {site}")
        else:
            print(Fore.GREEN + f"[FOUND] {site}: {url}")

# ===================== MAIN =====================
if __name__ == "__main__":
    banner()
    menu()
