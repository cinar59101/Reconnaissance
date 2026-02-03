__tool__ = "Reconnaissance"
__version__ = "1.1"
__author__ = "cinar59101"

# -*- coding: utf-8 -*-
import requests
from colorama import Fore, init
import sys
import time

init(autoreset=True)

HEADERS = {
    "User-Agent": "Reconnaissance-OSINT/1.1"
}

# ===================== BANNER =====================
def banner():
    print(Fore.CYAN + """
====================================
        Reconnaissance
     OSINT CLI Framework
        v1.1
====================================
""")

# ===================== MENU =====================
def menu():
    while True:
        print(Fore.YELLOW + """
[1] Username Reconnaissance
[0] Exit
""")
        try:
            choice = input(Fore.CYAN + "Seçim: ").strip()
        except KeyboardInterrupt:
            print(Fore.RED + "\nÇıkış yapıldı.")
            sys.exit(0)

        if choice == "1":
            username = input("Username: ").strip()
            if username:
                username_osint(username)
            else:
                print(Fore.RED + "Username boş olamaz.")
        elif choice == "0":
            print(Fore.GREEN + "Çıkış yapılıyor...")
            break
        else:
            print(Fore.RED + "Geçersiz seçim.")

# ===================== REQUEST HELPER =====================
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

# ===================== USERNAME OSINT =====================
def username_osint(username):
    print(Fore.CYAN + f"\n[+] Username Reconnaissance: {username}\n")

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
        "Twitter/X": {
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
        time.sleep(0.5)  # rate limit / termux dostu

        r = safe_request(data["url"])

        if r == "timeout":
            print(Fore.YELLOW + f"[TIMEOUT] {site}")
            continue
        if r == "error":
            print(Fore.MAGENTA + f"[ERROR] {site}")
            continue

        page = r.text.lower()

        # 🔴 Net NOT FOUND
        if r.status_code == 404 or any(x in page for x in data["not_found"]):
            print(Fore.RED + f"[NOT FOUND] {site}")

        # 🟢 Proof ile doğrulanmış FOUND
        elif r.status_code == 200 and any(p.lower() in page for p in data["proof"]):
            print(Fore.GREEN + f"[FOUND] {site}: {data['url']}")

        # 🟡 Belirsiz durum
        else:
            print(Fore.YELLOW + f"[UNKNOWN] {site}")

# ===================== MAIN =====================
if __name__ == "__main__":
    banner()
    menu()
