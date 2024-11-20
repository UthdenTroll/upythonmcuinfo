import os
import sys
import machine
import gc
import time

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


def pin_info():
    """Displays information about each pin's configuration."""
    print("\n=== Pin Configuration Info ===")
    
    max_pins = 40  # Adjust this based on your MCU
    for pin_num in range(max_pins):
        try:
            pin = machine.Pin(pin_num)
            pin_mode = "Mode=" + str(pin.mode()) if hasattr(pin, 'mode') else "Mode=NA"
            pin_pull = "Pull=" + str(pin.pull()) if hasattr(pin, 'pull') else "Pull=NA"

            print(f"Pin {pin_num}: {pin_mode}, {pin_pull}")
        except ValueError:
            # Skip invalid or nonexistent pins
            continue
        except AttributeError:
            print(f"Pin {pin_num}: NA")


if __name__ == "__main__":
    mcu_info()
    pin_info()
