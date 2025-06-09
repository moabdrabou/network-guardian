import nmap
import time
import schedule
from datetime import datetime
from config import NETWORK_SCAN_RANGE, SCAN_INTERVAL_MINUTES
from database import setup_database, get_known_devices, add_known_device, log_scan_event
from notifier import send_notification

def scan_network():
    """
    Scans the network for active devices and returns a list of dictionaries
    containing MAC, IP, and hostname.
    """
    nm = nmap.PortScanner()
    print(f"Starting network scan on {NETWORK_SCAN_RANGE}...")
    log_scan_event(f"Starting network scan on {NETWORK_SCAN_RANGE}...")

    # -sn (ping scan) is faster and doesn't scan ports, just checks if hosts are up.
    # We might need to adjust this depending on the network setup and desired detail.
    # For more detailed info including MAC/Hostname, we often need -O (OS detection) or -A (aggressive)
    # or just rely on ARP cache for local network, which nmap often does with -sn on local subnet.
    # Let's use a combination for reliable MAC/hostname detection.
    # nmap.scan() is usually asynchronous. .wait() is needed.
    # Using 'sudo' might be required for accurate MAC address detection depending on OS/config.
 
    try:
        # If run without sudo, nmap might not be able to get MAC addresses reliably.
        # Adding '-n' (no DNS resolution) speeds it up if hostnames aren't critical initially.
        nm.scan(hosts=NETWORK_SCAN_RANGE, arguments='-sn') # -sn for ping scan (host discovery)
    except nmap.PortScannerError as e:
        print(f"Nmap scan error: {e}. Make sure nmap is installed and accessible.")
        print("You might need to run this script with 'sudo' for full functionality (especially MAC address detection).")
        log_scan_event(f"Nmap scan error: {e}")
        return []

    active_devices = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]['addresses']['mac']
            ip_address = nm[host]['addresses']['ipv4']
            hostname = nm[host]['hostnames'][0]['name'] if nm[host]['hostnames'] else 'N/A'
            active_devices.append({
                'mac': mac_address.upper(), # Standardize MAC to uppercase
                'ip': ip_address,
                'hostname': hostname
            })
    print(f"Scan completed. Found {len(active_devices)} active devices.")
    log_scan_event(f"Scan completed. Found {len(active_devices)} active devices.")
    return active_devices

def manage_devices():
    """
    Compares current active devices with known devices, notifies of unknowns,
    and logs current network state.
    """
    active_devices = scan_network()
    known_macs = get_known_devices()

    current_scan_macs = {device['mac'] for device in active_devices}

    # Identify unknown devices
    unknown_devices = []
    for device in active_devices:
        if device['mac'] not in known_macs:
            unknown_devices.append(device)

    if unknown_devices:
        message = "🚨 NEW UNKNOWN DEVICES DETECTED ON NETWORK! 🚨\n"
        log_scan_event("!!! NEW UNKNOWN DEVICES DETECTED ON NETWORK !!!")
        for device in unknown_devices:
            msg_line = f"  MAC: {device['mac']}, IP: {device['ip']}, Hostname: {device['hostname']}"
            message += msg_line + "\n"
            log_scan_event(f"  Unknown Device: {msg_line}")
        send_notification(message)
    else:
        print("No new unknown devices detected.")
        log_scan_event("No new unknown devices detected.")

    # Log all currently active devices for inventory/record
    log_scan_event("\n--- Current Active Devices (Inventory) ---")
    for device in active_devices:
        log_scan_event(f"  MAC: {device['mac']}, IP: {device['ip']}, Hostname: {device['hostname']}")
    log_scan_event("----------------------------------------\n")

    # Important: This part requires manual interaction initially.
    # You need to manually add devices to 'known_devices.db' after the first scan.
    # You can do this by running `python main.py` once, then checking the logs,
    # and then using `database.add_known_device()` in an interactive session
    # or a separate script to populate your initial known devices.
    # For initial setup, you might manually edit known_devices.db or
    # run a script that prompts you to add newly found devices.
    # Example: add_known_device("AA:BB:CC:DD:EE:FF", "192.168.1.100", "MyLaptop", "My personal laptop")



if __name__ == "__main__":
    setup_database() # Ensure database is set up

    print(f"Network scanner initialized. Scanning every {SCAN_INTERVAL_MINUTES} minutes.")
    print("Press Ctrl+C to stop.")

    # Run immediately on startup
    manage_devices()

    # Schedule the scan to run periodically
    schedule.every(SCAN_INTERVAL_MINUTES).minutes.do(manage_devices)

    while True:
        schedule.run_pending()
        time.sleep(1) # Wait for 1 second before checking scheduled tasks again