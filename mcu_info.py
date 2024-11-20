import os
import sys
import machine
import gc
import time
import json

# Load the pinout database
def load_pinout_database(file_path="mcu_pinoutdatabase.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Pinout database not found!")
        return {}
    except json.JSONDecodeError:
        print("Error decoding the pinout database!")
        return {}

# Display general MCU information
def mcu_info():
    """Displays general MCU information."""
    print("=== MCU Specifications ===")
    print(f"MicroPython Version: {sys.version}")
    print(f"Machine: {os.uname().machine}")
    print(f"Processor: {os.uname().sysname}")
    print(f"Release Version: {os.uname().release}")
    print(f"RAM Free: {gc.mem_free()} bytes")

    try:
        flash_size = os.statvfs('/')
        print(f"Flash Size: {flash_size[0] * flash_size[2]} bytes")
    except Exception:
        print("Flash Size: NA")

    print("\n=== Hardware Info ===")
    try:
        print(f"Frequency: {machine.freq()} Hz")
    except AttributeError:
        print("Frequency: NA")

    print("\n=== Time Info ===")
    try:
        print(f"Uptime: {time.ticks_ms() // 1000} seconds since boot")
    except AttributeError:
        print("Uptime: NA")

# Display pin configuration
def pin_info(database):
    """Displays information about each pin's configuration."""
    print("\n=== Pin Configuration Info ===")
    
    detected_mcu = os.uname().machine.split(" ")[0]  # Extract the MCU name
    pinout = database.get(detected_mcu, None)
    if not pinout:
        print(f"Pinout not found for MCU: {detected_mcu}")
        return

    max_pins = 40  # Adjust this based on your MCU
    for pin_num in range(max_pins):
        pin_name = f"GPIO{pin_num}"  # Default GPIO naming
        description = pinout.get(pin_name, "Unknown")

        try:
            pin = machine.Pin(pin_num)
            pin_mode = "Mode=" + str(pin.mode()) if hasattr(pin, 'mode') else "Mode=NA"
            pin_pull = "Pull=" + str(pin.pull()) if hasattr(pin, 'pull') else "Pull=NA"
            print(f"{pin_name}: {description}, {pin_mode}, {pin_pull}")
        except ValueError:
            # Skip invalid or nonexistent pins
            continue
        except AttributeError:
            print(f"{pin_name}: {description}, NA")

if __name__ == "__main__":
    pinout_database = load_pinout_database()  # Load the pinout database
    mcu_info()  # Display MCU info
    pin_info(pinout_database)  # Display pin information
