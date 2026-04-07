"""
Network Diagnostic & Monitoring Tool
Author: Nandini Jampana
Description: Monitors internal intranet nodes via ping checks and port scanning.
             Generates an HTML report and logs results with timestamps.
"""

import socket
import subprocess
import logging
import os
import platform
from datetime import datetime
from jinja2 import Template

# ── CONFIG ──────────────────────────────────────────────────────────────────
HOSTS_FILE = "hosts.txt"
LOG_FILE = "monitor.log"
REPORT_FILE = "report.html"
PORTS_TO_CHECK = [80, 443, 22, 8080]  # Common ports to scan
PING_COUNT = 2  # Number of ping attempts

# ── LOGGING SETUP ────────────────────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# ── FUNCTIONS ────────────────────────────────────────────────────────────────

def load_hosts(filepath):
    """Load list of hosts/IPs from file, skip comments and blank lines."""
    if not os.path.exists(filepath):
        logging.error(f"Hosts file '{filepath}' not found.")
        return []
    hosts = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(",")
                ip = parts[0].strip()
                label = parts[1].strip() if len(parts) > 1 else ip
                hosts.append({"ip": ip, "label": label})
    return hosts


def ping_host(ip):
    """Ping a host and return True if reachable."""
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", str(PING_COUNT), "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", str(PING_COUNT), "-W", "1", ip]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception as e:
        logging.warning(f"Ping error for {ip}: {e}")
        return False


def check_port(ip, port, timeout=2):
    """Check if a specific port is open on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def resolve_hostname(ip):
    """Try to resolve IP to hostname."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "N/A"


def monitor_hosts(hosts):
    """Run diagnostics on all hosts and return results."""
    results = []
    logging.info(f"Starting diagnostics for {len(hosts)} host(s)...")

    for host in hosts:
        ip = host["ip"]
        label = host["label"]
        logging.info(f"Checking {label} ({ip})...")

        ping_status = ping_host(ip)
        hostname = resolve_hostname(ip)

        port_results = {}
        for port in PORTS_TO_CHECK:
            port_results[port] = check_port(ip, port)

        overall = "UP" if ping_status else "DOWN"
        logging.info(f"  → {label} ({ip}): {overall}")

        results.append({
            "label": label,
            "ip": ip,
            "hostname": hostname,
            "ping": ping_status,
            "ports": port_results,
            "status": overall,
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return results


# ── HTML REPORT TEMPLATE ─────────────────────────────────────────────────────

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Network Diagnostic Report</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; color: #2d3748; padding: 30px; }
    h1 { font-size: 24px; color: #2b6cb0; margin-bottom: 4px; }
    .meta { font-size: 13px; color: #718096; margin-bottom: 28px; }
    table { width: 100%; border-collapse: collapse; background: white;
            border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
    th { background: #2b6cb0; color: white; padding: 13px 16px; text-align: left; font-size: 13px; }
    td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid #e2e8f0; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #f7fafc; }
    .badge { display: inline-block; padding: 3px 10px; border-radius: 20px;
             font-size: 11px; font-weight: 600; }
    .up   { background: #c6f6d5; color: #276749; }
    .down { background: #fed7d7; color: #9b2c2c; }
    .open   { background: #bee3f8; color: #2c5282; }
    .closed { background: #e2e8f0; color: #718096; }
    .summary { display: flex; gap: 16px; margin-bottom: 24px; }
    .card { background: white; border-radius: 10px; padding: 18px 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07); flex: 1; text-align: center; }
    .card .num { font-size: 32px; font-weight: 700; }
    .card .lbl { font-size: 12px; color: #718096; margin-top: 4px; }
    .green { color: #38a169; } .red { color: #e53e3e; } .blue { color: #3182ce; }
  </style>
</head>
<body>
  <h1>🌐 Network Diagnostic Report</h1>
  <div class="meta">Generated on: {{ generated_at }} &nbsp;|&nbsp; Total Hosts: {{ results|length }}</div>

  <div class="summary">
    <div class="card"><div class="num blue">{{ results|length }}</div><div class="lbl">Total Hosts</div></div>
    <div class="card"><div class="num green">{{ results | selectattr('status','eq','UP') | list | length }}</div><div class="lbl">Hosts Up</div></div>
    <div class="card"><div class="num red">{{ results | selectattr('status','eq','DOWN') | list | length }}</div><div class="lbl">Hosts Down</div></div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Label</th>
        <th>IP Address</th>
        <th>Hostname</th>
        <th>Ping</th>
        {% for port in ports %}
        <th>Port {{ port }}</th>
        {% endfor %}
        <th>Status</th>
        <th>Checked At</th>
      </tr>
    </thead>
    <tbody>
      {% for r in results %}
      <tr>
        <td><strong>{{ r.label }}</strong></td>
        <td>{{ r.ip }}</td>
        <td>{{ r.hostname }}</td>
        <td><span class="badge {{ 'up' if r.ping else 'down' }}">{{ 'OK' if r.ping else 'FAIL' }}</span></td>
        {% for port in ports %}
        <td><span class="badge {{ 'open' if r.ports[port] else 'closed' }}">{{ 'Open' if r.ports[port] else 'Closed' }}</span></td>
        {% endfor %}
        <td><span class="badge {{ 'up' if r.status == 'UP' else 'down' }}">{{ r.status }}</span></td>
        <td>{{ r.checked_at }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""

def generate_report(results):
    """Render HTML report from results."""
    template = Template(HTML_TEMPLATE)
    html = template.render(
        results=results,
        ports=PORTS_TO_CHECK,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    with open(REPORT_FILE, "w") as f:
        f.write(html)
    logging.info(f"Report saved to '{REPORT_FILE}'")


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n==============================")
    print("  Network Diagnostic Tool")
    print("==============================\n")

    hosts = load_hosts(HOSTS_FILE)
    if not hosts:
        print("No hosts found. Please add entries to hosts.txt")
        exit(1)

    results = monitor_hosts(hosts)
    generate_report(results)

    up = sum(1 for r in results if r["status"] == "UP")
    down = len(results) - up

    print(f"\n✅ Done! {up} UP / {down} DOWN")
    print(f"📄 Report: {REPORT_FILE}")
    print(f"📋 Log:    {LOG_FILE}\n")
