import keyboard as kb
import win32gui
import win32con
import win32api
import pywintypes
from config import char_legend, game_name


def focus_window(title):
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        print(f"Window not found: {title}")
        return

    # Check if minimized, then restore if it is
    placement = win32gui.GetWindowPlacement(hwnd)
    is_minimized = (placement[1] == win32con.SW_SHOWMINIMIZED)

    if is_minimized:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Bring window to foreground
    win32gui.BringWindowToTop(hwnd)
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  # ALT down
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)  # ALT up

    #the following is used 
    try:
        win32gui.SetForegroundWindow(hwnd)
    except pywintypes.error:
        print(f"Windows blocked foreground for: {title}")

    #I used the following for troubleshooting. Uncomment it if you want
#    print(f"Focused: {title}")

def handle_hotkey(event):
    char_name = char_legend.get(event.name)
    if char_name:
        title = f"{char_name} - {game_name}"
        focus_window(title)
    return False  # suppress key

# Register hotkeys with the suppression
for key in char_legend:
    kb.on_press_key(key, lambda e, k=key: handle_hotkey(e), suppress=True)

print("Listening for hotkeys...")
kb.wait()
