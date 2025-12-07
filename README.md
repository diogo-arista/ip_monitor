# IP Monitor

A simple Python script to monitor changes to your public IP address.

## Features

- **Continuous Monitoring**: Checks your public IP every 60 seconds.
- **Logging**: Records IP history and changes in `logs/changes.log`.
- **Notifications**: Sends a desktop notification when your IP address changes.
- **Instant Check**: Ability to run a one-time check of your current IP details.

## Prerequisites

- Python installed on your Windows machine.
- Required Python packages:
  ```powershell
  pip install requests plyer
  ```

## How to use in Windows

### 1. Start Monitoring (Visible)
To start the script in a visible terminal window:

1. Open a terminal (PowerShell or Command Prompt).
2. Navigate to the folder containing the script.
3. Run:
   ```powershell
   python ip_monitor.py
   ```
4. **Keep this terminal window open** to keep the script running.

### 2. Start Monitoring (Background)
To run the script silently in the background (no open window):

1. Use `pythonw` instead of `python`:
   ```powershell
      pythonw ip_monitor.py
   ```
2. The script will start and run in the background.

### 3. Check IP Instantly
To see your current IP details without monitoring:

```powershell
python ip_monitor.py --now
```

## How to check if it is running

### If running visibly:
- **Check your Taskbar**: Look for the open Command Prompt or PowerShell window.

### If running in background:
- **PowerShell**: Run the following command to see if the process is active:
  ```powershell
  Get-Process pythonw
  ```
- **Task Manager**:
  1. Open Task Manager (`Ctrl+Shift+Esc`).
  2. Go to the **Details** tab.
  3. Look for `pythonw.exe`.

## How to stop it

### If running visibly:
- **Keyboard Shortcut**: Click into the terminal window and press `Ctrl+C`.
- **Close Window**: Simply close the terminal window.

### If running in background:
- **PowerShell**:
  ```powershell
  Stop-Process -Name pythonw
  ```
  *Note: This will stop ALL running pythonw scripts.*

- **Task Manager**:
  1. Find `pythonw.exe` in the **Details** tab.
  2. Right-click it and select **End Task**.
