import time
import os
import logging
import requests
import argparse
from datetime import datetime
from plyer import notification
import platform
import subprocess

# --- Configuration ---
CHECK_INTERVAL = 15  # Seconds between checks in monitor mode
LOG_FILE_PATH = os.path.join("logs", "changes.log")
IP_API_URL = "http://ip-api.com/json/"

def setup_logger():
    """Sets up the logging directory and configuration."""
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def get_ip_data():
    """Fetches public IP and location data."""
    try:
        response = requests.get(IP_API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Only print error if running in interactive check mode, otherwise silent
        return None

def send_notification():
    """Sends a system notification."""
    try:
        if platform.system() == "Darwin":
            # macOS native notification
            script = 'display notification "IP Changed" with title "IP Monitor"'
            subprocess.run(["osascript", "-e", script])
        else:
            # Fallback/Default for Windows/Linux
            notification.notify(
                title="IP Monitor",
                message="IP Changed",
                app_name="IP Monitor",
                timeout=10
            )
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")

def get_last_ip():
    """Reads the last known IP from the log file."""
    if not os.path.exists(LOG_FILE_PATH):
        return None
    try:
        with open(LOG_FILE_PATH, 'r') as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "IP Changed to:" in line:
                    parts = line.split("IP Changed to: ")
                    if len(parts) > 1:
                        return parts[1].split(" ")[0].strip()
    except Exception:
        return None
    return None

def run_monitor_mode():
    """Runs the continuous monitoring loop."""
    setup_logger()
    print(f"Monitoring started. Checking every {CHECK_INTERVAL} seconds...")
    print(f"Logs: {os.path.abspath(LOG_FILE_PATH)}")
    
    current_ip = get_last_ip()

    while True:
        data = get_ip_data()
        
        if data and data.get('status') == 'success':
            new_ip = data.get('query')
            city = data.get('city', 'Unknown')
            country = data.get('country', 'Unknown')
            
            logging.info(f"Check performed. Current IP: {new_ip} | Location: {city}, {country}")

            if new_ip and new_ip != current_ip:
                log_message = f"IP Changed to: {new_ip} | Location: {city}, {country}"
                logging.info(log_message)
                print(f"[{datetime.now()}] CHANGE DETECTED: {log_message}")
                send_notification()
                current_ip = new_ip
        
        time.sleep(CHECK_INTERVAL)

def run_check_mode():
    """Runs a single on-demand check and prints to console."""
    print("Checking current IP...", end="\r")
    data = get_ip_data()
    
    if data and data.get('status') == 'success':
        print("\n" + "="*40)
        print(f" CURRENT IP : {data.get('query')}")
        print(f" LOCATION   : {data.get('city')}, {data.get('country')}")
        print(f" ISP        : {data.get('isp')}")
        print("="*40 + "\n")
    else:
        print("\nError: Could not fetch IP data. Check your connection.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor Public IP or Check it once.")
    parser.add_argument("--now", action="store_true", help="Check IP immediately and exit")
    
    args = parser.parse_args()

    if args.now:
        run_check_mode()
    else:
        run_monitor_mode()