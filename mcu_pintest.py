# Explanation
# For Each Pin:
#
# PULL_UP: 
# Indicates the state of the pin when configured with an internal pull-up resistor (which forces the pin to a logical HIGH state when no external signal is connected).
# Expected output:
# 1: The pin correctly defaults to HIGH when the pull-up resistor is enabled.
# 0: The pin incorrectly reads as LOW, which could indicate an issue with the pull-up resistor or its configuration.
#
# PULL_DOWN:
# Indicates the state of the pin when configured with an internal pull-down resistor (which forces the pin to a logical LOW state when no external signal is connected).
# Expected output:
# 0: The pin correctly defaults to LOW when the pull-down resistor is enabled.
# 1: The pin incorrectly reads as HIGH, which could indicate an issue with the pull-down resistor or its configuration.
#
# OUT_HIGH:
# Reflects the pin's value when set to output mode and explicitly driven HIGH.
# Expected output:
# 1: The pin was successfully set to HIGH.
# 0: The pin failed to set to HIGH, which could indicate an issue with the output mode or internal circuitry.
#
# OUT_LOW:
# Reflects the pin's value when set to output mode and explicitly driven LOW.
# Expected output:
# 0: The pin was successfully set to LOW.
# 1: The pin failed to set to LOW, which could indicate an issue with the output mode or internal circuitry.

# Error Messages:
# Test failed (ValueError: Pin does not exist):
# Indicates that the pin is not valid for the MCU being tested. This typically happens when the script attempts to access a pin number that does not exist on the board.
#
# What the Results Mean
# Normal Operation:
#
# If a pin outputs PULL_UP=1, PULL_DOWN=0, OUT_HIGH=1, and OUT_LOW=0, it means:
# The internal pull-up resistor is functional.
# The internal pull-down resistor is functional.
# The pin can switch between HIGH and LOW in output mode.
#
# Abnormal Behavior:
# If the results deviate from the expected values, it may indicate:
# Hardware damage to the pin.
# A conflict with a peripheral using the pin (e.g., UART, I2C).
# Incorrect firmware or board configuration.
#
# Nonexistent Pins:
# Pins that don't exist on the MCU will trigger an error and be skipped.
#
# How to Use the Results
# Identify Valid Pins:
# Use this output to find which pins are available and functional for your project.
# Verify MCU Health:
# Check for pins that fail the tests to detect hardware issues.
# Diagnose Firmware Issues:
# If all pins fail, there could be an issue with the firmware or the pin initialization.

import machine

def pin_scan(max_pins):
    for pin_num in range(max_pins):
        try:
            print(f"\nTesting Pin {pin_num}...")
            
            # Test pull resistors
            pin = machine.Pin(pin_num, machine.Pin.IN, machine.Pin.PULL_UP)
            pull_up_value = pin.value()
            pin = machine.Pin(pin_num, machine.Pin.IN, machine.Pin.PULL_DOWN)
            pull_down_value = pin.value()

            # Test output
            pin = machine.Pin(pin_num, machine.Pin.OUT)
            pin.value(1)
            high_value = pin.value()
            pin.value(0)
            low_value = pin.value()

            # Report results
            print(f"Pin {pin_num}: PULL_UP={pull_up_value}, PULL_DOWN={pull_down_value}, OUT_HIGH={high_value}, OUT_LOW={low_value}")
        
        except Exception as e:
            print(f"Pin {pin_num}: Test failed ({e})")

# Scan up to 40 pins
pin_scan(40)
