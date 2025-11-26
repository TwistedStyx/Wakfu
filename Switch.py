import keyboard as kb
import win32gui
import win32con
import win32api
import pywintypes
from config import char_legend, game_name


window_cache = {}

def get_window_handle(title):
    hwnd = window_cache.get(title)
    if hwnd and win32gui.IsWindow(hwnd):
        return hwnd
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        window_cache[title] = hwnd
    return hwnd

def focus_window(title):
    hwnd = get_window_handle(title)
    if not hwnd:
        print(f"Window not found: {title}")
        return

    # Restore if minimized
    placement = win32gui.GetWindowPlacement(hwnd)
    is_minimized = (placement[1] == win32con.SW_SHOWMINIMIZED)
    if is_minimized:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Bring to foreground
    win32gui.BringWindowToTop(hwnd)

    # Helps to bypass windows BS
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

    try:
        win32gui.SetForegroundWindow(hwnd)
    except pywintypes.error:
        print(f"Windows prevented focus for: {title}")

def handle_hotkey(event):
    char_name = char_legend.get(event.name)
    if char_name:
        title = f"{char_name} - {game_name}"
        focus_window(title)
    return False  # suppress original key

# Register hotkeys
for key in char_legend:
    kb.on_press_key(key, lambda e, k=key: handle_hotkey(e), suppress=True)

print("Listening for hotkeys...")
kb.wait()
