"""
hardware.py — Hardware abstraction for Cadodile Jungle Trivia
Supports real Raspberry Pi hardware OR automatic stub mode.
Never crashes if libraries are missing.
"""

import time
import threading
from config import (
    LED_GPIO, SERVO_CHANNEL, SERVO_CENTER,
    DISPENSE_OPEN_ANGLE, DISPENSE_CLOSED_ANGLE,
    DISPENSE_OPEN_TIME_SEC, DISPENSE_PAUSE_SEC,
)

# ── Globals ──
_stub_mode = True
_led = None
_servo_kit = None


def init_hardware(stub_mode: bool = False):
    """
    Initialize hardware. If stub_mode is True or libraries are missing,
    all calls become print-only stubs. Never crashes.
    """
    global _stub_mode, _led, _servo_kit

    if stub_mode:
        _stub_mode = True
        print("[HARDWARE] Stub mode enabled (forced).")
        return

    # Try importing real hardware libraries
    try:
        from gpiozero import LED as GPIOLed
        _led = GPIOLed(LED_GPIO)
        print(f"[HARDWARE] LED initialized on GPIO {LED_GPIO}.")
    except Exception as e:
        print(f"[HARDWARE] LED unavailable: {e}")
        _led = None

    try:
        from adafruit_servokit import ServoKit
        _servo_kit = ServoKit(channels=16)
        _servo_kit.servo[SERVO_CHANNEL].angle = SERVO_CENTER
        print(f"[HARDWARE] Servo initialized on channel {SERVO_CHANNEL}.")
    except Exception as e:
        print(f"[HARDWARE] Servo unavailable: {e}")
        _servo_kit = None

    # If both failed, we're effectively in stub mode
    _stub_mode = (_led is None and _servo_kit is None)
    if _stub_mode:
        print("[HARDWARE] No hardware detected — running in stub mode.")
    else:
        print("[HARDWARE] Hardware ready.")


def set_led(on: bool):
    """Turn LED on or off."""
    if _led:
        _led.on() if on else _led.off()
    else:
        print(f"[STUB] LED {'ON' if on else 'OFF'}")


def blink_led(duration_sec: float = 1.0):
    """Blink the LED for a duration (non-blocking)."""
    def _blink():
        end = time.time() + duration_sec
        while time.time() < end:
            set_led(True)
            time.sleep(0.15)
            set_led(False)
            time.sleep(0.15)
    threading.Thread(target=_blink, daemon=True).start()


def set_servo_angle(angle: int):
    """Set servo to a specific angle (0–180)."""
    angle = max(0, min(180, angle))
    if _servo_kit:
        _servo_kit.servo[SERVO_CHANNEL].angle = angle
    else:
        print(f"[STUB] Servo → {angle} degrees")


def dispense_block():
    """
    Activate the servo to dispense one block.
    Runs in a background thread so it never blocks the UI.
    """
    def _dispense():
        print("[HARDWARE] Dispensing block...")
        set_servo_angle(DISPENSE_OPEN_ANGLE)
        time.sleep(DISPENSE_OPEN_TIME_SEC)
        set_servo_angle(DISPENSE_CLOSED_ANGLE)
        time.sleep(DISPENSE_PAUSE_SEC)
        set_servo_angle(SERVO_CENTER)
        blink_led(1.0)
        print("[HARDWARE] Dispense complete.")
    threading.Thread(target=_dispense, daemon=True).start()


def stop_all():
    """Reset all hardware to safe state."""
    set_led(False)
    set_servo_angle(SERVO_CENTER)
    print("[HARDWARE] All hardware stopped.")
