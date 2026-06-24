# ==================== УНИВЕРСАЛЬНЫЙ GLOBAL МЬЮТЕКС ====================
import sys
import ctypes
import atexit

def _init_system_wide_mutex():
    kernel32 = ctypes.windll.kernel32
    clean_name = os.path.basename(sys.argv[0]).replace('.', '_').replace(' ', '_')
    mutex_name = f"Global\\AutoGuard_{clean_name}_Mutex"
    mutex_handle = kernel32.CreateMutexW(None, False, mutex_name)
    
    if kernel32.GetLastError() == 183:
        if mutex_handle:
            kernel32.CloseHandle(mutex_handle)
            
        try:
            is_russian = ctypes.windll.kernel32.GetUserDefaultUILanguage() == 1049
        except Exception:
            is_russian = True
            
        if is_russian:
            msg = "Приложение уже запущено!\nРазрешена только одна активная копия."
            title = "Защита от повторного запуска"
        else:
            msg = "The application is already running!\nOnly one active instance is allowed."
            title = "Already Running"
            
        ctypes.windll.user32.MessageBoxW(0, msg, title, 0x10 | 0x00)
        sys.exit(0)
        
    atexit.register(lambda: kernel32.CloseHandle(mutex_handle) if mutex_handle else None)

import os
_init_system_wide_mutex()
# ======================================================================

import random
import string
import sys
import webbrowser
import math
import atexit
import ctypes
import customtkinter as ctk
from tkinter import messagebox

# ==================== КОНСТАНТЫ ====================
ENTROPY_WEAK_THRESHOLD = 42.0
ENTROPY_MEDIUM_THRESHOLD = 58.0
PENALTY_SINGLE_TYPE = 0.75
BONUS_MAX_DIVERSITY = 12.0
NORMALIZER = 75.0

MUTEX_NAME = "Local\\KiziName_Gen-Password_v1.0_Mutex"

# ==================== ЗАЩИТА ОТ ВТОРОГО ЗАПУСКА (Windows) ====================
kernel32 = ctypes.windll.kernel32
mutex_handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
if kernel32.GetLastError() == 183:
    messagebox.showerror("Ошибка", "Программа уже запущена!")
    sys.exit(0)

atexit.register(lambda: kernel32.CloseHandle(mutex_handle) if mutex_handle else None)

# ==================== НАСТРОЙКИ ИНТЕРФЕЙСА ====================
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# ==================== ЛОКАЛИЗАЦИЯ ====================
LANGUAGES = {
    "ru": {
        "title": "Gen-Password",
        "length_lbl": "Длина пароля (4-20):",
        "btn_gen": "Сгенерировать",
        "btn_copy": "Копировать",
        "copied": "Скопировано!",
        "about_btn": "О программе",
        "about_text": "Автор: KiziName\nВерсия: v1.0",
        "about_title": "О программе",
        "error_text": "Ошибка: Введите число от 4 до 20!",
        "error_no_cb": "Ошибка: Выберите хотя бы один пункт!",
        "cb_letters": "Буквы (a-Z)",
        "cb_digits": "Цифры (0-9)",
        "cb_symbols": "Символы (%@#$)",
        "strength_weak": "Слабый пароль",
        "strength_medium": "Средний пароль",
        "strength_strong": "Надёжный пароль"
    },
    "en": {
        "title": "Gen-Password",
        "length_lbl": "Password length (4-20):",
        "btn_gen": "Generate",
        "btn_copy": "Copy",
        "copied": "Copied!",
        "about_btn": "About",
        "about_text": "Author: KiziName\nVersion: v1.0",
        "about_title": "About",
        "error_text": "Error: Enter a number between 4 and 20!",
        "error_no_cb": "Error: Select at least one option!",
        "cb_letters": "Letters (a-Z)",
        "cb_digits": "Digits (0-9)",
        "cb_symbols": "Symbols (%@#$)",
        "strength_weak": "Weak password",
        "strength_medium": "Medium password",
        "strength_strong": "Strong password"
    }
}

current_lang = "ru"
GITHUB_URL = "https://github.com/KIziName/Gen-Password/releases"
last_error_type = None  # "length" или "no_cb"

# ==================== ЛОГИКА ПРОГРАММЫ ====================
def check_strength(length, pool_size):
    if pool_size == 0 or length == 0:
        return 0.0, "", "#333333"

    entropy = length * math.log2(pool_size)
    active_types = sum([cb_letters_var.get(), cb_digits_var.get(), cb_symbols_var.get()])

    if active_types == 1:
        entropy *= PENALTY_SINGLE_TYPE
    elif active_types == 3 and length >= 8:
        entropy += BONUS_MAX_DIVERSITY

    progress = min(entropy / NORMALIZER, 1.0)

    if entropy < ENTROPY_WEAK_THRESHOLD:
        return progress, LANGUAGES[current_lang]["strength_weak"], "#FF3B30"
    elif entropy < ENTROPY_MEDIUM_THRESHOLD:
        return progress, LANGUAGES[current_lang]["strength_medium"], "#FFCC00"
    else:
        return progress, LANGUAGES[current_lang]["strength_strong"], "#4CAF50"

def generate_password():
    global last_error_type
    label_error.configure(text="")
    last_error_type = None
    btn_copy.configure(text=LANGUAGES[current_lang]["btn_copy"], fg_color=default_copy_color)

    pbar_strength.set(0)
    lbl_strength.configure(text="", text_color="white")

    try:
        length = int(entry_length.get())
        if length < 4 or length > 20:
            label_error.configure(text=LANGUAGES[current_lang]["error_text"])
            last_error_type = "length"
            entry_result.configure(state="normal")
            entry_result.delete(0, 'end')
            entry_result.configure(state="readonly")
            return
    except ValueError:
        label_error.configure(text=LANGUAGES[current_lang]["error_text"])
        last_error_type = "length"
        entry_result.configure(state="normal")
        entry_result.delete(0, 'end')
        entry_result.configure(state="readonly")
        return

    pool = ""
    pool_size = 0
    if cb_letters_var.get():
        pool += string.ascii_letters
        pool_size += 52
    if cb_digits_var.get():
        pool += string.digits
        pool_size += 10
    if cb_symbols_var.get():
        pool += string.punctuation
        pool_size += len(string.punctuation)

    if not pool:
        label_error.configure(text=LANGUAGES[current_lang]["error_no_cb"])
        last_error_type = "no_cb"
        entry_result.configure(state="normal")
        entry_result.delete(0, 'end')
        entry_result.configure(state="readonly")
        return

    password = ''.join(random.choice(pool) for _ in range(length))
    entry_result.configure(state="normal")
    entry_result.delete(0, 'end')
    entry_result.insert(0, password)
    entry_result.configure(state="readonly")

    progress, text, color = check_strength(length, pool_size)
    pbar_strength.set(progress)
    pbar_strength.configure(progress_color=color)
    lbl_strength.configure(text=text, text_color=color)

def copy_to_clipboard():
    password = entry_result.get()
    if password:
        app.clipboard_clear()
        app.clipboard_append(password)
        app.update()
        btn_copy.configure(text=LANGUAGES[current_lang]["copied"], fg_color="#4CAF50")

def open_github():
    webbrowser.open_new_tab(GITHUB_URL)

def show_about():
    about_win = ctk.CTkToplevel(app)
    about_win.title(LANGUAGES[current_lang]["about_title"])
    about_win.geometry("260x140")
    about_win.resizable(False, False)
    about_win.attributes("-topmost", True)

    about_win.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - (about_win.winfo_width() // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (about_win.winfo_height() // 2)
    about_win.geometry(f"+{x}+{y}")

    lbl = ctk.CTkLabel(about_win, text=LANGUAGES[current_lang]["about_text"], justify="center", font=("Arial", 12))
    lbl.pack(pady=(15, 5))

    lbl_link = ctk.CTkLabel(about_win, text="GitHub Releases", font=("Arial", 12, "underline"), text_color="#1F6AA5", cursor="hand2")
    lbl_link.pack(pady=5)
    lbl_link.bind("<Button-1>", lambda e: open_github())

def switch_language():
    global current_lang, last_error_type
    current_lang = "en" if current_lang == "ru" else "ru"

    app.title(LANGUAGES[current_lang]["title"])
    label_length.configure(text=LANGUAGES[current_lang]["length_lbl"])
    btn_generate.configure(text=LANGUAGES[current_lang]["btn_gen"])
    btn_about.configure(text=LANGUAGES[current_lang]["about_btn"])
    btn_lang.configure(text="RU" if current_lang == "ru" else "EN")
    cb_letters.configure(text=LANGUAGES[current_lang]["cb_letters"])
    cb_digits.configure(text=LANGUAGES[current_lang]["cb_digits"])
    cb_symbols.configure(text=LANGUAGES[current_lang]["cb_symbols"])
    btn_copy.configure(text=LANGUAGES[current_lang]["btn_copy"])

    if entry_result.get():
        try:
            length = int(entry_length.get())
            pool_size = (52 if cb_letters_var.get() else 0) + (10 if cb_digits_var.get() else 0) + (len(string.punctuation) if cb_symbols_var.get() else 0)
            progress, text, color = check_strength(length, pool_size)
            lbl_strength.configure(text=text, text_color=color)
            pbar_strength.set(progress)
        except ValueError:
            pass  # Если длина некорректна, просто ничего не меняем
    else:
        pbar_strength.set(0)
        lbl_strength.configure(text="")

    if last_error_type == "length":
        label_error.configure(text=LANGUAGES[current_lang]["error_text"])
    elif last_error_type == "no_cb":
        label_error.configure(text=LANGUAGES[current_lang]["error_no_cb"])

# ==================== ГЛАВНОЕ ОКНО ====================
app = ctk.CTk()
app.title(LANGUAGES[current_lang]["title"])
app.geometry("400x510")
app.resizable(False, False)

top_frame = ctk.CTkFrame(app, fg_color="transparent")
top_frame.pack(fill="x", padx=10, pady=10)

btn_lang = ctk.CTkButton(top_frame, text="RU", width=40, command=switch_language)
btn_lang.pack(side="left")

btn_about = ctk.CTkButton(top_frame, text=LANGUAGES[current_lang]["about_btn"], width=100, command=show_about)
btn_about.pack(side="right")

label_length = ctk.CTkLabel(app, text=LANGUAGES[current_lang]["length_lbl"], font=("Arial", 14))
label_length.pack(pady=(5, 5))

entry_length = ctk.CTkEntry(app, width=60, justify="center")
entry_length.insert(0, "12")
entry_length.pack(pady=5)

cb_frame = ctk.CTkFrame(app, fg_color="transparent")
cb_frame.pack(pady=10)

cb_letters_var = ctk.BooleanVar(value=True)
cb_letters = ctk.CTkCheckBox(cb_frame, text=LANGUAGES[current_lang]["cb_letters"], variable=cb_letters_var)
cb_letters.pack(anchor="w", pady=4)

cb_digits_var = ctk.BooleanVar(value=True)
cb_digits = ctk.CTkCheckBox(cb_frame, text=LANGUAGES[current_lang]["cb_digits"], variable=cb_digits_var)
cb_digits.pack(anchor="w", pady=4)

cb_symbols_var = ctk.BooleanVar(value=True)
cb_symbols = ctk.CTkCheckBox(cb_frame, text=LANGUAGES[current_lang]["cb_symbols"], variable=cb_symbols_var)
cb_symbols.pack(anchor="w", pady=4)

label_error = ctk.CTkLabel(app, text="", font=("Arial", 12, "bold"), text_color="#FF3B30")
label_error.pack(pady=2)

btn_generate = ctk.CTkButton(app, text=LANGUAGES[current_lang]["btn_gen"], font=("Arial", 14, "bold"), command=generate_password)
btn_generate.pack(pady=5)

entry_result = ctk.CTkEntry(app, width=280, justify="center", font=("Arial", 14), state="readonly")
entry_result.pack(pady=10)

lbl_strength = ctk.CTkLabel(app, text="", font=("Arial", 12, "bold"))
lbl_strength.pack(pady=(5, 2))

pbar_strength = ctk.CTkProgressBar(app, width=200, height=8, corner_radius=4)
pbar_strength.set(0)
pbar_strength.pack(pady=(0, 10))

btn_copy = ctk.CTkButton(app, text=LANGUAGES[current_lang]["btn_copy"], font=("Arial", 12), width=120, fg_color="#333333", command=copy_to_clipboard)
btn_copy.pack(pady=5)

default_copy_color = btn_copy.cget("fg_color")

app.mainloop()
