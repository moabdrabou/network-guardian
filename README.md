# 🌐✨ Network Guardian: Device Scanner & Notifier

A **Python-based project** designed to enhance your home network security by continuously monitoring for unknown or unauthorized devices. Leveraging `nmap` and `python-nmap`, this tool acts as your personal network security watchdog and inventory manager, alerting you when new devices join your network.

---

## 🚀 Features

* **Network Discovery:** Uses `python-nmap` to reliably scan your local network for active devices, capturing their IP address, MAC address, and hostname.
* **Device Whitelisting:** Maintains a secure SQLite database (`known_devices.db`) to store a list of your authorized, known devices.
* **Intruder Detection:** Compares active devices against your whitelist and immediately alerts you to any new or unauthorized connections.
* **Configurable Notifications:** Supports console output, Pushover notifications, and can be extended for email alerts.
* **Device Inventory:** Logs all detected devices with timestamps for comprehensive network record-keeping.
* **Scheduled Scans:** Automatically runs scans at configurable intervals (e.g., every 10 minutes) to ensure continuous monitoring.

---

## 🛠️ Prerequisites

Before you get started, make sure you have the following installed:

* **Python 3.x:** Download from [python.org](https://www.python.org/downloads/).
* **Nmap:** The network scanning utility.
    * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install nmap`
    * **macOS (Homebrew):** `brew install nmap`
    * **Windows:** Download the installer from [nmap.org/download.html](https://nmap.org/download.html). Ensure it's added to your system's PATH.

---

## 📦 Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/moabdrabou/network-guardian.git
    ```

    ```bash
    cd network-guardian
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install python-nmap requests schedule
    ```

---

## ⚙️ Configuration

Open `config.py` and modify the following settings:

* **`NETWORK_SCAN_RANGE`**: **Crucial!** Set this to your local network's IP range in CIDR notation (e.g., `'192.168.1.0/24'`). You can usually find this by checking your router's default gateway IP or your computer's local IP address and subnet mask.
* **Notification Settings**:
    * **Pushover:** If you want real-time mobile alerts, set `ENABLE_PUSHOVER = True` and replace `'YOUR_PUSHOVER_USER_KEY'` and `'YOUR_PUSHOVER_API_TOKEN'` with your actual keys from [pushover.net](https://pushover.net/).
    * **Email (Optional):** If you wish to use email notifications, uncomment the relevant lines in `config.py` and `notifier.py` and fill in your SMTP server details, sender/receiver emails, and password.
* **`SCAN_INTERVAL_MINUTES`**: Adjust how often the network scan runs (default is 10 minutes).

---

## 🚀 Usage

### 1. Initial Setup & Populating Known Devices

First, you need to tell the system which devices are *known* and *authorized*.

1.  **Run an Initial Scan:**
    Open your terminal or command prompt in the project directory.

    * **On Linux/macOS:** You **might need `sudo`** for `nmap` to reliably capture MAC addresses.
        ```bash
        sudo python3 main.py
        ```
    * **On Windows (or if `sudo` is not required):**
        ```bash
        python main.py
        ```
    The script will perform an initial scan and print detected devices to the console. It will also create a `logs` directory with `scan_log.txt` containing a detailed record.

2.  **Identify Your Known Devices:**
    Review the console output or `logs/scan_log.txt`. Note down the **MAC addresses, IP addresses, and hostnames** of all your legitimate devices (router, personal laptop, phone, smart TV, smart bulbs, etc.).

3.  **Add Known Devices to the Database:**
    You'll manually populate your `known_devices.db` database using the `add_known_device` function.

    **Option A (Recommended for beginners): Create a temporary script**
    Create a new Python file (e.g., `add_my_devices.py`) in the project's root directory (or the `network_scanner` directory) with the following content, replacing the example values with your actual device details:

    ```python
    # add_my_devices.py
    from database import add_known_device, setup_database

    setup_database() # Ensure the database table exists

    print("Adding your known devices...")

    # --- Add your devices below (replace with your actual device details!) ---
    # Example:
    add_known_device("00:11:22:33:44:55", "192.168.1.1", "MyRouter", "Main Home Router")
    add_known_device("AA:BB:CC:DD:EE:FF", "192.168.1.10", "MyLaptop", "My personal laptop")
    add_known_device("11:22:33:44:55:66", "192.168.1.15", "MyPhone", "My smartphone")
    add_known_device("DE:AD:BE:EF:00:01", "192.168.1.20", "SmartBulb1", "Living Room Smart Bulb")
    # Add all your other devices similarly!
    # --- End of your devices ---

    print("Known devices added/updated successfully.")
    print("You can now run 'main.py' for continuous monitoring.")
    ```
    Save `add_my_devices.py` and run it:
    ```bash
    python3 add_my_devices.py
    ```
    (You don't need `sudo` for this specific script.)

    **Option B (Advanced): Using a SQLite Browser**
    You can use a tool like [DB Browser for SQLite](https://sqlitebrowser.org/) to directly open `known_devices.db` and manually insert rows into the `known_devices` table.

### 2. Running for Continuous Monitoring

Once your `known_devices.db` is populated with your authorized devices, you can run the main script to start continuous monitoring:

```bash
# On Linux/macOS (potentially with sudo)
sudo python3 main.py

# On Windows (or if sudo not needed)
python main.py