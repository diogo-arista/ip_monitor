# IP Monitor - Code Explained

This document explains how the `ip_monitor.py` script works, step by step. It is designed for beginners to understand what each part of the code does.

## 1. Imports

At the very top of the file, we import specific libraries (modules) that give us extra functionality.

```python
import time
import os
import logging
import requests
import argparse
from datetime import datetime
from plyer import notification
import platform
import subprocess
```

*   `time`: Used to make the script "sleep" (wait) for a certain amount of time.
*   `os`: Helps us interact with the operating system (like checking if folders exist).
*   `logging`: Used to save messages to a file (our `changes.log`).
*   `requests`: Allows us to "visit" a website (API) to ask for our IP address.
*   `argparse`: Helps us read command-line arguments (like `--now`).
*   `datetime`: Gives us the current date and time.
*   `plyer` & `notification`: This is what shows the popup bubble on your screen.
*   `platform` & `subprocess`: Used to detect if you are on Windows or Mac to show the right kind of notification.

## 2. Configuration

Here we set up some "constants" (values that we use later).

```python
CHECK_INTERVAL = 15  
LOG_FILE_PATH = os.path.join("logs", "changes.log")
IP_API_URL = "http://ip-api.com/json/"
```

*   `CHECK_INTERVAL`: How many seconds to wait between checks (currently 15 seconds).
*   `LOG_FILE_PATH`: Where we will save the log file. It puts it inside a `logs` folder.
*   `IP_API_URL`: The website address we ask for IP information.

## 3. Setting up the Logger (`setup_logger`)

```python
def setup_logger():
    # ... checks if 'logs' folder exists, creates it if not ...
    # ... sets up the file format for logging ...
```

This function makes sure the `logs` folder exists. If it doesn't, it creates it. It also tells Python how to format the lines in the log file (adding the date and time automatically).

## 4. Getting IP Data (`get_ip_data`)

```python
def get_ip_data():
    try:
        response = requests.get(IP_API_URL, timeout=10)
        # ... checks if request was successful ...
        return response.json()
    except requests.RequestException:
        return None
```

This is the core of the script. It sends a message to the internet asking "What is my IP?".
*   If it works, it returns the data (IP, City, Country, etc.).
*   If the internet is down or it fails, it returns `None` (nothing), so the script doesn't crash.

## 5. Sending Notifications (`send_notification`)

```python
def send_notification():
    # ... checks if on Mac or Windows ...
    # ... shows the popup "IP Changed" ...
```

This function simply triggers the popup bubble on your screen. It handles both Windows (using `plyer`) and Mac (using `osascript`) separately.

## 6. Logic: Monitoring Mode (`run_monitor_mode`)

This is the main "loop" that runs forever in the background.

```python
def run_monitor_mode():
    setup_logger()
    # ... prints startup messages ...
    
    current_ip = get_last_ip() # Remembers the last IP if possible

    while True: # This loops forever!
        data = get_ip_data() # Check current IP
        
        # ... extracts the IP, city, country ...
            
        logging.info(...) # Write to log file that we checked

        if new_ip != current_ip: # DID IT CHANGE?
            # 1. Write the CHANGE to the log
            # 2. Print it to the console
            # 3. Send the notification popup
            current_ip = new_ip # Update our memory
        
        time.sleep(CHECK_INTERVAL) # Wait for 15 seconds before repeating
```

1.  It starts the logger.
2.  It enters a `while True` loop, which means it repeats forever until you stop it.
3.  Inside the loop:
    *   It checks the IP.
    *   It logs that it checked.
    *   **Crucially**: It asks "Is this IP different from the last one I saw?"
    *   If yes -> It logs the change and shows the notification.
    *   Finally, it `sleep`s (waits) for 15 seconds.

## 7. Logic: Check Mode (`run_check_mode`)

```python
def run_check_mode():
    # ... checks IP once ...
    # ... prints it nicely to the screen ...
```

This runs when you use `--now`. It doesn't loop; it just checks once, prints the result, and finishes.

## 8. The Entry Point

```python
if __name__ == "__main__":
    # ... reads arguments ...
    if args.now:
        run_check_mode()
    else:
        run_monitor_mode()
```

This is where the script actually starts when you run `python ip_monitor.py`.
*   It checks if you added `--now`.
*   If yes, it runs `run_check_mode()`.
*   If no, it runs `run_monitor_mode()`.
