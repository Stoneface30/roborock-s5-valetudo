"""
Roborock S5 — Automated UART Root Handler
==========================================
Key insight: U-Boot reads ONE character from the UART buffer at "run key detect".
Space (0x20) was found but ignored. This script tries specific trigger characters
to find which one changes the boot path (recovery / fastboot / U-Boot shell).

Characters tried in order each boot:
  '1' (0x31) → usually triggers recovery boot on Allwinner
  '2' (0x32) → usually triggers fastboot
  '3' (0x33) → sometimes triggers U-Boot shell
  '4' (0x34)
  'r' (0x72) → recovery on some builds
  'f' (0x66) → fastboot on some builds
  ESC (0x1b)
  Ctrl+C (0x03)

Just reconnect power for each attempt — script advances to next character automatically.

Once we get a shell (#), SSH is unlocked automatically.
SSH: root@192.168.0.202  password: valetudo123
"""

import serial
import threading
import sys
import time
import re
from datetime import datetime

PORT = "COM4"
BAUD = 115200

# Documented method: Allwinner S5 U-Boot key_detect script checks for 's' over UART.
# Must be flooding 's' before and through the entire boot sequence.
TRY_CHARS = [(b's', "s key — documented U-Boot entry method for Roborock S5")]

attempt = [0]  # mutable so thread can update it

STATE = "WAITING"
STATE_LOCK = threading.Lock()
flooding = [True]

# ── Helpers ───────────────────────────────────────────────────────────────────
def ts():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def log(msg):
    border = "=" * 62
    print(f"\n{border}\n[{ts()}] {msg}\n{border}\n", flush=True)

def send(ser, cmd, delay=1.0):
    print(f"[{ts()}] >>> {cmd}", flush=True)
    ser.write((cmd + "\r\n").encode())
    time.sleep(delay)


# ── Flood thread ──────────────────────────────────────────────────────────────
def flood_thread(ser):
    """
    Flood UART with the current attempt character until key_detect fires.
    This ensures the character is in the RX buffer when U-Boot reads it.
    """
    char, label = TRY_CHARS[attempt[0] % len(TRY_CHARS)]
    log(f"Attempt {attempt[0]+1}: Flooding with {repr(char)} [{label}]\nConnect power now.")
    while flooding[0]:
        try:
            ser.write(char)
            time.sleep(0.008)
        except Exception:
            break


# ── SSH unlock ────────────────────────────────────────────────────────────────
def run_ssh_unlock(ser):
    global STATE
    with STATE_LOCK:
        if STATE in ("INIT_SHELL", "DONE"):
            return
        STATE = "INIT_SHELL"

    log("SHELL DETECTED — Running SSH unlock...")

    send(ser, "while true; do echo V > /dev/watchdog; sleep 5; done &", delay=1.5)
    send(ser, "mount -o remount,rw /", delay=1.0)
    send(ser, "sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config", delay=0.8)
    send(ser, "sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config", delay=0.8)
    send(ser, "grep -q '^PermitRootLogin' /etc/ssh/sshd_config || echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config", delay=0.8)
    send(ser, "echo 'root:valetudo123' | chpasswd", delay=0.8)
    send(ser, "/etc/init.d/S50sshd restart 2>/dev/null || /usr/sbin/sshd 2>/dev/null || echo 'sshd attempted'", delay=2.0)
    send(ser, "netstat -tlnp 2>/dev/null | grep ':22' || ss -tlnp 2>/dev/null | grep ':22' || echo 'port check done'", delay=1.0)
    send(ser, "echo '>>> DONE <<<'", delay=0.5)

    STATE = "DONE"
    log(
        "SSH UNLOCK COMPLETE!\n\n"
        "  ssh root@192.168.0.202\n"
        "  password: valetudo123\n\n"
        "  (Wait 10 seconds if not immediately up)"
    )


# ── U-Boot override ───────────────────────────────────────────────────────────
def run_uboot_override(ser):
    global STATE
    with STATE_LOCK:
        if STATE != "WAITING":
            return
        STATE = "UBOOT_CMD_SENT"

    flooding[0] = False
    log("U-BOOT SHELL CAUGHT — Injecting init=/bin/sh...")
    time.sleep(0.3)
    send(ser, "setenv bootargs_extra 'init=/bin/sh'", delay=0.8)
    send(ser, "boot", delay=0.5)

    with STATE_LOCK:
        STATE = "KERNEL_BOOTING"
    log("Kernel booting with init override — waiting for shell...")


# ── Line processor ────────────────────────────────────────────────────────────
def process_line(ser, line):
    global STATE

    with STATE_LOCK:
        current = STATE

    stripped = line.strip()

    # ── U-Boot shell ───────────────────────────────────────────────────────
    if current == "WAITING" and re.search(r'sunxi#|sun8i#|SUNXI#', stripped, re.IGNORECASE):
        flooding[0] = False
        threading.Thread(target=run_uboot_override, args=(ser,), daemon=True).start()
        return

    # ── Show what character U-Boot found at key_detect ─────────────────────
    if 'no key input' in line or re.match(r'\s*0x[0-9a-fA-F]+\s*$', stripped):
        char, label = TRY_CHARS[attempt[0] % len(TRY_CHARS)]
        found = stripped if stripped != 'no key input' else '(nothing)'
        print(f"\n[{ts()}] key_detect saw: {found}  (we sent: {repr(char)} = {label})", flush=True)
        return

    # ── key_detect shows a DIFFERENT response → possible trigger found ─────
    if 'flag_recovery: 0x1' in line:
        flooding[0] = False
        log("RECOVERY MODE TRIGGERED! Watching for recovery shell...")
        with STATE_LOCK:
            STATE = "KERNEL_BOOTING"
        return

    # ── Init shell indicators ──────────────────────────────────────────────
    if current in ("KERNEL_BOOTING", "UBOOT_CMD_SENT"):
        hints = ["can't access tty", "job control turned off", "Freeing init memory"]
        if any(h in line for h in hints):
            print(f"[{ts()}] Init/recovery booting...", flush=True)
            return

    # ── Shell prompt ───────────────────────────────────────────────────────
    is_prompt = (
        re.match(r'^(/[^ ]*)?\s*#\s*$', stripped)
        or re.match(r'^sh[-\w.]*[#$]\s*$', stripped)
    )
    if is_prompt and current not in ("INIT_SHELL", "DONE", "WAITING"):
        threading.Thread(target=run_ssh_unlock, args=(ser,), daemon=True).start()
        return

    # ── Normal Linux boot ──────────────────────────────────────────────────
    if 'rockrobo login:' in line and current == "WAITING":
        flooding[0] = False
        char, label = TRY_CHARS[attempt[0] % len(TRY_CHARS)]
        attempt[0] += 1
        next_char, next_label = TRY_CHARS[attempt[0] % len(TRY_CHARS)]

        log(
            f"Normal boot — char {repr(char)} [{label}] had no effect.\n\n"
            f"  Next attempt #{attempt[0]+1}: {repr(next_char)} [{next_label}]\n\n"
            f"  Disconnect battery, wait 3 seconds, reconnect.\n"
            f"  Script will auto-flood with new character."
        )

        # Reset for next boot
        with STATE_LOCK:
            STATE = "WAITING"
        flooding[0] = True
        threading.Thread(target=flood_thread, args=(ser,), daemon=True).start()
        return


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 62)
    print(" ROBOROCK S5 — UART KEY FINDER + AUTO-ROOT")
    print("=" * 62)
    print()
    print(f" Port: {PORT}  Baud: {BAUD}")
    print()
    print(" HOW IT WORKS:")
    print("  U-Boot reads ONE character from UART at boot.")
    print("  Space was ignored. This script tries trigger characters.")
    print("  It advances automatically on each boot attempt.")
    print()
    print(" WHAT TO DO:")
    print("  1. Close PuTTY")
    print("  2. Run this script")
    print("  3. Wait for 'Connect power now' message")
    print("  4. Connect battery")
    print("  5. If normal boot: disconnect, wait 3s, reconnect")
    print("     Script auto-advances to next character")
    print()
    print(" Characters to try:", ", ".join(f"{repr(c)} ({l})" for c, l in TRY_CHARS))
    print()
    print("=" * 62)
    print()

    try:
        ser = serial.Serial(PORT, BAUD, timeout=0.1)
    except Exception as e:
        print(f"ERROR: {e}")
        print("Is PuTTY still open? Close it first.")
        sys.exit(1)

    # Start flooding immediately
    threading.Thread(target=flood_thread, args=(ser,), daemon=True).start()

    line_buf = ""

    try:
        while True:
            data = ser.read(512)
            if data:
                text = data.decode("utf-8", errors="replace")
                print(text, end="", flush=True)
                line_buf += text
                while "\n" in line_buf:
                    line, line_buf = line_buf.split("\n", 1)
                    process_line(ser, line)
            else:
                time.sleep(0.01)

    except KeyboardInterrupt:
        flooding[0] = False
        print("\nExiting.")
        ser.close()
    except Exception as e:
        flooding[0] = False
        print(f"\nError: {e}")
        ser.close()


if __name__ == "__main__":
    main()
