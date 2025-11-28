import tkinter as tk
from tkinter import messagebox
import psutil
import win32gui
import win32con
import win32api
import win32process
import pywintypes
import keyboard as kb
from config import game_name, cycle_key


window_list = []
current_index = -1

def find_game_windows(title_text):
    matched = []
    def enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)

        if not title.lower().endswith(title_text.lower()):
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            exe = psutil.Process(pid).name().lower()
            if exe == "java.exe":
                matched.append((hwnd, title))
        except:
            pass
    win32gui.EnumWindows(enum_handler, None)
    return matched

def get_window_list():
    global window_list, current_index
    window_list = find_game_windows(game_name)
    current_index = -1
    update_window_listbox()

def focus_window(hwnd):
    if not hwnd or not win32gui.IsWindow(hwnd):
        return

    placement = win32gui.GetWindowPlacement(hwnd)
    if placement[1] == win32con.SW_SHOWMINIMIZED:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.BringWindowToTop(hwnd)

    # ALT trick for SetForegroundWindow
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

    try:
        win32gui.SetForegroundWindow(hwnd)
    except pywintypes.error:
        pass

def cycle_windows():
    global current_index, window_list
    total = len(window_list)
    if total == 0:
        messagebox.showinfo("Info", "No matching game windows found.")
        return

    current_index += 1
    if current_index >= total:
        current_index = 0

    hwnd, title = window_list[current_index]
    focus_window(hwnd)
    status_var.set(f"Focusing: {title.rstrip(" - WAKFU")}")
    #update_window_listbox() Want to test before I uncomment
    highlight_current_window()

def handle_cycle(_):
    cycle_windows()
    return False  # suppress key

# GUI Setup
root = tk.Tk()
root.title("Wakfu Multi")
root.geometry("300x300")
root.configure(bg="#2b2b2b")  # Dark background

# Status label
status_var = tk.StringVar()
status_var.set("Ready")
status_label = tk.Label(root, textvariable=status_var, anchor="w",
                        bg="#2b2b2b", fg="#c0c0c0")
status_label.pack(fill="x", padx=5, pady=5)

# Window listbox
listbox = tk.Listbox(root, bg="#3c3f41", fg="#c0c0c0",
                     selectbackground="#5a5c5e", selectforeground="#c0c0c0")
listbox.pack(fill="both", expand=True, padx=5, pady=5)

def update_window_listbox():
    listbox.delete(0, tk.END)
    for hwnd, title in window_list:
        listbox.insert(tk.END, title)

def highlight_current_window():
    listbox.selection_clear(0, tk.END)
    if 0 <= current_index < len(window_list):
        listbox.selection_set(current_index)
        listbox.see(current_index)

# Buttons frame
button_frame = tk.Frame(root, bg="#2b2b2b")
button_frame.pack(fill="x", pady=5)

def style_button(btn):
    btn.configure(bg="#3c3f41", fg="#c0c0c0",
                  activebackground="#5a5c5e", activeforeground="#c0c0c0",
                  relief="flat")

refresh_btn = tk.Button(button_frame, text="Refresh Windows", command=get_window_list)
cycle_btn = tk.Button(button_frame, text="Cycle Window", command=cycle_windows)
refresh_btn.pack(side="left", padx=5)
cycle_btn.pack(side="left", padx=5)

style_button(refresh_btn)
style_button(cycle_btn)


if __name__ == "__main__":
    get_window_list()
    kb.on_press_key(cycle_key, handle_cycle, suppress=True)

    root.mainloop()

