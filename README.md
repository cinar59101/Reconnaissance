# Reconnaissance

🕵️ **Reconnaissance** is a terminal-based OSINT (Open Source Intelligence) tool written in Python.
It is designed for **ethical, educational, and defensive security research** purposes.

The tool currently focuses on **username reconnaissance**, detecting whether a specific username exists across multiple popular platforms while minimizing false positives.

---

## 🚀 Features

* 🔍 Username OSINT (GitHub, Instagram, Twitter/X, TikTok, Reddit)
* 🧠 Site-specific content verification (not just HTTP status codes)
* ❌ Reduced false positives (no simple substring matching)
* 🖥️ Terminal-based interactive menu
* ⚡ Fast and lightweight

---

## 📦 Requirements

* Python **3.9+** recommended

Python libraries used:

```
requests
colorama
python-whois
requests
colorama

```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Reconnaissance/
│
├── reconnaissance.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## ▶️ Usage

Run the tool from the terminal:

```bash
python reconnaissance.py
```

You will see an interactive menu:

```
[1] Username Reconnaissance
[2] Check for updates
[0] Exit
```

Enter a username and the tool will check supported platforms.

---

## 🧪 Example Output

```
[+] Username Reconnaissance: exampleuser

[FOUND] GitHub: https://github.com/exampleuser
[NOT FOUND] Instagram
[UNKNOWN] Twitter/X
[NOT FOUND] Reddit
```

---

## ⚠️ Ethical Notice

This tool is intended **only for ethical OSINT purposes**, such as:

* Learning OSINT techniques
* Defensive security research
* Personal account audits

❌ Do **NOT** use this tool for harassment, stalking, or illegal activities.

The author is **not responsible for misuse** of this software.

---

## 🛠️ Roadmap

Planned improvements:

* Confidence score system
* JSON / TXT report export
* `--username` CLI argument support
* Deep / fast scan modes
* More platforms (50+)

---

## 👤 Author

* GitHub: **cinar59101**
* With The Assistance Of: **Chatgpt**

---

## 📄 License

This project is licensed under the **MIT License**.



