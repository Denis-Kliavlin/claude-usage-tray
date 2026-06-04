# -*- coding: utf-8 -*-
"""Claude Usage Tray - system tray monitor for Claude API usage."""

VERSION = "1.4.0"

import json
import subprocess
import threading
import time
import sys
import os
import msvcrt
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

LOCK_FILE = os.path.join(os.environ.get("TEMP", "C:/tmp"), "claude-usage-tray.lock")

import pystray
from PIL import Image, ImageDraw, ImageFont
from winotify import Notification, audio

# --- Config ---
CHROME_BRIDGE = os.environ.get("CHROME_BRIDGE_URL", "http://localhost:3456")
ORG_ID = os.environ.get("CLAUDE_ORG_ID", "")
POLL_INTERVAL = int(os.environ.get("CLAUDE_POLL_INTERVAL", "60"))
THRESHOLDS = [70, 80, 90]
APP_ID = "Claude Usage Monitor"
ICON_SIZE = 64
WORKING_DIR = os.environ.get("CLAUDE_WORKING_DIR", os.path.expanduser("~"))

# State
state = {
    "five_hour": {"utilization": 0, "resets_at": None},
    "seven_day": {"utilization": 0, "resets_at": None},
    "extra_usage": {"used_credits": 0, "monthly_limit": 0, "utilization": 0},
    "last_update": None,
    "error": None,
    "notified_5h": set(),
    "notified_7d": set(),
    "prev_5h": 0,
    "prev_7d": 0,
}


def fetch_usage():
    """Fetch usage via Chrome Bridge execute -> fetchData."""
    payload = json.dumps({
        "browser": "chrome",
        "url": "https://claude.ai/settings",
        "autoClose": True,
        "actions": [
            {
                "type": "fetchData",
                "fetchUrl": f"/api/organizations/{ORG_ID}/usage",
            }
        ],
        "timeout": 30000,
    }).encode()

    req = Request(
        f"{CHROME_BRIDGE}/execute",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read())
    except (URLError, TimeoutError, json.JSONDecodeError) as e:
        state["error"] = str(e)
        return False

    if not data.get("success"):
        state["error"] = data.get("error", "unknown")
        return False

    results = data.get("result", {}).get("results", [])
    if not results or not results[0].get("ok"):
        state["error"] = "API returned error"
        return False

    api = results[0]["data"]

    for key in ("five_hour", "seven_day"):
        if api.get(key):
            state[key]["utilization"] = api[key].get("utilization") or 0
            state[key]["resets_at"] = api[key].get("resets_at")

    if api.get("extra_usage"):
        state["extra_usage"] = {
            "used_credits": api["extra_usage"].get("used_credits") or 0,
            "monthly_limit": api["extra_usage"].get("monthly_limit") or 0,
            "utilization": api["extra_usage"].get("utilization") or 0,
        }

    state["last_update"] = datetime.now().strftime("%H:%M")
    state["error"] = None
    return True


def format_reset_time(resets_at, short=False):
    """Format time until reset: '4h 21m' or 'Wed 20:00' for >24h."""
    if not resets_at:
        return "?"
    try:
        reset_dt = datetime.fromisoformat(resets_at)
        now = datetime.now(timezone.utc)
        delta = reset_dt - now
        total_sec = max(0, int(delta.total_seconds()))
        hours = total_sec // 3600
        minutes = (total_sec % 3600) // 60
        if hours >= 24:
            local_dt = reset_dt.astimezone()
            day = local_dt.strftime("%a")
            return f"{day} {local_dt.strftime('%H:%M')}"
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    except (ValueError, TypeError):
        return "?"


def build_tooltip():
    """Build tooltip text."""
    u5 = state["five_hour"]["utilization"]
    u7 = state["seven_day"]["utilization"]
    r5 = format_reset_time(state["five_hour"]["resets_at"])
    r7 = format_reset_time(state["seven_day"]["resets_at"])

    lines = [
        f"Session: {u5}% | Resets {r5}",
        f"Weekly: {u7}% | Resets {r7}",
    ]

    eu = state["extra_usage"]
    if eu.get("monthly_limit"):
        used = eu['used_credits'] / 100
        limit = eu['monthly_limit'] / 100
        lines.append(f"Extra: ${used:.2f}/${limit:.0f} ({eu.get('utilization', 0)}%)")

    if state["error"]:
        lines.append(f"ERR: {state['error'][:30]}")
    elif state["last_update"]:
        lines.append(f"Upd: {state['last_update']}")

    return "\n".join(lines)


def menu_session_text(item):
    """Dynamic menu text for session usage."""
    u = state["five_hour"]["utilization"]
    r = format_reset_time(state["five_hour"]["resets_at"])
    return f"Session: {u}% (resets {r})"


def menu_weekly_text(item):
    """Dynamic menu text for weekly usage."""
    u = state["seven_day"]["utilization"]
    r = format_reset_time(state["seven_day"]["resets_at"])
    return f"Weekly: {u}% (resets {r})"


def menu_extra_text(item):
    """Dynamic menu text for extra usage."""
    eu = state["extra_usage"]
    if eu.get("monthly_limit"):
        used = eu['used_credits'] / 100
        limit = eu['monthly_limit'] / 100
        return f"Extra: ${used:.2f} / ${limit:.0f} ({eu.get('utilization', 0)}%)"
    return "Extra: off"


def get_color(pct):
    """Icon color by percent: green -> yellow -> orange -> red."""
    if pct < 50:
        return (76, 175, 80)
    if pct < 70:
        return (255, 193, 7)
    if pct < 85:
        return (255, 152, 0)
    return (244, 67, 54)


def create_icon_image(pct):
    """Create tray icon with percentage number."""
    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    color = get_color(pct)
    draw.ellipse([2, 2, ICON_SIZE - 2, ICON_SIZE - 2], fill=color)

    text = str(int(pct))
    try:
        font = ImageFont.truetype("arial.ttf", 28 if pct < 100 else 22)
    except (OSError, IOError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (ICON_SIZE - tw) // 2
    y = (ICON_SIZE - th) // 2 - 2
    draw.text((x, y), text, fill=(255, 255, 255), font=font)

    return img


def send_notification(title, message):
    """Send Windows toast notification."""
    try:
        toast = Notification(
            app_id=APP_ID,
            title=title,
            msg=message,
            duration="short",
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except Exception as e:
        print(f"Notification error: {e}", file=sys.stderr)


def check_thresholds():
    """Check thresholds and send notifications."""
    checks = [
        ("Session", "five_hour", "notified_5h", "prev_5h"),
        ("Weekly", "seven_day", "notified_7d", "prev_7d"),
    ]
    for label, key, notified_key, prev_key in checks:
        pct = state[key]["utilization"]
        prev = state[prev_key]
        reset_time = format_reset_time(state[key]["resets_at"])
        notified = state[notified_key]

        # Limits refreshed: was >=100% and now <100%
        if prev >= 100 and pct < 100:
            send_notification(
                f"Claude {label}: limits refreshed!",
                f"Now {pct}% used. Tokens available again!",
            )

        for threshold in THRESHOLDS:
            if pct >= threshold and threshold not in notified:
                notified.add(threshold)
                send_notification(
                    f"Claude {label}: {pct}%",
                    f"Used {pct}% of limit. Resets in {reset_time}.",
                )

        # Reset notifications when utilization drops (after reset)
        if pct < min(THRESHOLDS):
            notified.clear()

        state[prev_key] = pct


def update_icon(icon):
    """Update icon image and tooltip based on current state."""
    pct = state["five_hour"]["utilization"]
    try:
        icon.icon = create_icon_image(pct)
        icon.title = build_tooltip()
    except Exception:
        pass


def poll_loop(icon):
    """Background polling loop."""
    while getattr(icon, '_running', True):
        ok = fetch_usage()
        if ok:
            check_thresholds()
        update_icon(icon)

        for _ in range(POLL_INTERVAL):
            if not getattr(icon, '_running', True):
                return
            time.sleep(1)


def on_open_claude(icon, item):
    """Double-click: open Claude Desktop app."""
    subprocess.Popen(
        ["cmd", "/c", "start", "shell:AppsFolder\\Claude_pzs8sxrjxfjjc!Claude"],
        creationflags=0x00000008,
    )


def on_open_claude_code(icon, item):
    """Open Claude Code CLI in working directory."""
    subprocess.Popen(
        ["cmd", "/c", "start", "Claude Code", "cmd", "/k", f"cd /d {WORKING_DIR} && claude"],
        creationflags=0x00000008,
    )


def on_refresh(icon, item):
    """Manual refresh."""
    ok = fetch_usage()
    if ok:
        check_thresholds()
    update_icon(icon)


def on_quit(icon, item):
    icon._running = False
    icon.stop()


def acquire_lock():
    """Prevent duplicate instances via lock file."""
    try:
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        return fd
    except (OSError, IOError):
        sys.exit(0)  # already running


def main():
    if not ORG_ID:
        print("ERROR: Set CLAUDE_ORG_ID environment variable. "
              "Find it at claude.ai/settings → URL contains /organizations/<ORG_ID>/",
              file=sys.stderr)
        sys.exit(1)

    lock_fd = acquire_lock()
    fetch_usage()
    check_thresholds()

    pct = state["five_hour"]["utilization"]

    icon = pystray.Icon(
        "claude-usage",
        icon=create_icon_image(pct),
        title=build_tooltip(),
        menu=pystray.Menu(
            pystray.MenuItem(menu_session_text, None, enabled=False),
            pystray.MenuItem(menu_weekly_text, None, enabled=False),
            pystray.MenuItem(menu_extra_text, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Open Claude", on_open_claude, default=True),
            pystray.MenuItem("Open Claude Code", on_open_claude_code),
            pystray.MenuItem("Refresh", on_refresh),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(f"v{VERSION}", None, enabled=False),
            pystray.MenuItem("Quit", on_quit),
        ),
    )
    icon._running = True

    t = threading.Thread(target=poll_loop, args=(icon,), daemon=True)
    t.start()

    icon.run()


if __name__ == "__main__":
    main()
