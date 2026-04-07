# 🌐 Network Diagnostic & Monitoring Tool

A lightweight Python utility to monitor internal intranet nodes via automated **ping checks** and **port scanning**. Generates a clean HTML status report and maintains a timestamped log file — built for enterprise intranet environments.

---

## 📸 Sample Report

| Label | IP | Ping | Port 80 | Port 443 | Status |
|---|---|---|---|---|---|
| Main Gateway | 192.168.1.1 | ✅ OK | ✅ Open | ✅ Open | 🟢 UP |
| Web Server | 192.168.1.10 | ✅ OK | ✅ Open | ❌ Closed | 🟢 UP |
| Database Server | 192.168.1.11 | ❌ FAIL | ❌ Closed | ❌ Closed | 🔴 DOWN |

---

## ✨ Features

- ✅ **Ping Check** — Verifies if a host is reachable on the network
- ✅ **Port Scanning** — Checks status of ports 80, 443, 22, 8080
- ✅ **Hostname Resolution** — Resolves IPs to hostnames automatically
- ✅ **HTML Report** — Auto-generates a visual UP/DOWN status report
- ✅ **Logging** — Timestamped logs saved to `monitor.log`
- ✅ **Configurable Hosts** — Easily add/remove hosts via `hosts.txt`
- ✅ **Cross-platform** — Works on Windows, Linux, and macOS

---

## 🗂️ Project Structure

```
network-diagnostic-tool/
├── monitor.py          # Main monitoring script
├── hosts.txt           # List of hosts/IPs to monitor
├── requirements.txt    # Python dependencies
├── report.html         # Auto-generated HTML report (after running)
├── monitor.log         # Auto-generated log file (after running)
└── README.md           # Project documentation
```

---

## ⚙️ Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/network-diagnostic-tool.git
cd network-diagnostic-tool
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure hosts
Edit `hosts.txt` and add your internal IPs or hostnames:
```
192.168.1.1, Main Gateway
192.168.1.10, Web Server
192.168.1.20, Mail Server
```

### 4. Run the tool
```bash
python monitor.py
```

### 5. View the report
Open `report.html` in any browser to see the visual status dashboard.

---

## 🕐 Schedule Automated Runs

### Linux/macOS (cron job — every 5 minutes)
```bash
crontab -e
# Add this line:
*/5 * * * * /usr/bin/python3 /path/to/monitor.py
```

### Windows (Task Scheduler)
1. Open **Task Scheduler** → Create Basic Task
2. Set trigger: **Every 5 minutes**
3. Action: `python C:\path\to\monitor.py`

---

## 🛠️ Configuration

You can change these settings at the top of `monitor.py`:

| Variable | Default | Description |
|---|---|---|
| `HOSTS_FILE` | `hosts.txt` | Path to hosts list |
| `LOG_FILE` | `monitor.log` | Path to log output |
| `REPORT_FILE` | `report.html` | Path to HTML report |
| `PORTS_TO_CHECK` | `[80, 443, 22, 8080]` | Ports to scan |
| `PING_COUNT` | `2` | Number of ping attempts |

---

## 📋 Sample Log Output

```
2024-01-15 10:30:01 | INFO | Starting diagnostics for 10 host(s)...
2024-01-15 10:30:01 | INFO | Checking Main Gateway (192.168.1.1)...
2024-01-15 10:30:02 | INFO |   → Main Gateway (192.168.1.1): UP
2024-01-15 10:30:02 | INFO | Checking Web Server (192.168.1.10)...
2024-01-15 10:30:03 | INFO |   → Web Server (192.168.1.10): UP
2024-01-15 10:30:03 | INFO | Checking Database Server (192.168.1.11)...
2024-01-15 10:30:05 | INFO |   → Database Server (192.168.1.11): DOWN
2024-01-15 10:30:05 | INFO | Report saved to 'report.html'
```

---

## 🧰 Tech Stack

- **Python 3.x**
- `socket` — Port scanning & hostname resolution
- `subprocess` — Ping execution
- `logging` — Log management
- `jinja2` — HTML report generation

---

## 👩‍💻 Author

**Nandini Jampana**  
Engineer | Cybersecurity & Network Administration  
📧 nandinijampana528@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
