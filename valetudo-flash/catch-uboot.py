"""
Roborock S5 U-Boot catcher
- Floods COM4 with space characters before/during power-on
- When U-Boot prompt appears (# or >) press Ctrl+C to stop flooding
- Then type U-Boot commands interactively
"""
import serial
import threading
import sys
import time

PORT = "COM4"
BAUD = 115200

print(f"Opening {PORT} at {BAUD}...")
try:
    ser = serial.Serial(PORT, BAUD, timeout=0.05)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

print("=" * 60)
print("PORT OPEN.")
print("NOW connect the battery / power on the robot.")
print("Press Ctrl+C when you see 'sunxi#' or '#' prompt.")
print("=" * 60)
print()

flooding = True
output_buf = []

def reader():
    while True:
        try:
            data = ser.read(256)
            if data:
                text = data.decode("utf-8", errors="replace")
                print(text, end="", flush=True)
                output_buf.append(text)
        except Exception:
            pass

t = threading.Thread(target=reader, daemon=True)
t.start()

# Flood phase — send spaces at 5ms intervals
try:
    count = 0
    while flooding:
        ser.write(b" ")
        count += 1
        time.sleep(0.005)
        if count % 200 == 0:
            # Every second, also send Enter and a newline
            ser.write(b"\r\n")
except KeyboardInterrupt:
    flooding = False
    print("\n\n>>> FLOOD STOPPED — interactive mode <<<")
    print("Type U-Boot commands. Press Enter after each.")
    print("First command to type: setenv bootargs_extra 'init=/bin/sh'")
    print()

# Interactive phase
while True:
    try:
        cmd = input()
        ser.write((cmd + "\r\n").encode())
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        ser.close()
        break
