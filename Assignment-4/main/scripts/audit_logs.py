import os
import re

LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'debug.log')


def audit_logs():
    if not os.path.exists(LOG_FILE):
        print(f"Log file not found at {LOG_FILE}")
        return

    print(f"Auditing logs at {LOG_FILE}...")
    with open(LOG_FILE, 'r') as file:
        for line in file:
            if re.search('suspicious|csrf', line, re.IGNORECASE):
                print(f"Suspicious Activity: {line.strip()}")


if __name__ == '__main__':
    audit_logs()
