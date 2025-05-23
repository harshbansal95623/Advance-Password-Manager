# 🔐 Advanced Password Manager (GUI-Based)

A secure and customizable password manager built with Python and Tkinter. This tool allows users to store, retrieve, and generate complex passwords with authentication and encryption-like behavior (via clipboard use and secure SQLite storage).

---

## 🛡️ Features

- 🔒 **Authentication System**: Secure access using a predefined passcode.
- 💾 **Save Passwords**: Store account credentials securely in an SQLite database.
- 🔍 **Retrieve Passwords**: Search for saved credentials and copy them to the clipboard.
- 🛠️ **Custom Password Generator**: Generate strong, complex passwords based on your own criteria.
- 👁️ **Toggle Visibility**: Show/hide password input fields for added privacy.
- 📋 **Clipboard Integration**: Automatically copy retrieved or generated passwords to your clipboard.

---

## 🧰 Tech Stack

- **Language**: Python 3
- **GUI Framework**: Tkinter
- **Database**: SQLite3
- **Other Libraries**: `pyperclip` for clipboard integration

---

## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/Harsh179Bansal/Advance-Password-Manager.git
cd Advance-Password-Manager
pip install -r requirements.txt
python3 password_manager.py
