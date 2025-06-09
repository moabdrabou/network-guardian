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