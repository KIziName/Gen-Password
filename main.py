import customtkinter as ctk
import webbrowser
import config
import logic

# Защита от повторного запуска
logic.init_system_wide_mutex()

# Настройки темы
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

current_lang = "ru"
last_error_type = None

def clear_result_entry():
    entry_result.configure(state="normal")
    entry_result.delete(0, 'end')
    entry_result.configure(state="readonly")

def generate_password():
    global last_error_type
    label_error.configure(text="")
    last_error_type = None
    btn_copy.configure(text=config.LANGUAGES[current_lang]["btn_copy"], fg_color=default_copy_color)

    pbar_strength.set(0)
    lbl_strength.configure(text="", text_color="white")

    try:
        length = int(entry_length.get())
        if length < 4 or length > 20:
            label_error.configure(text=config.LANGUAGES[current_lang]["error_text"])
            last_error_type = "length"
            clear_result_entry()
            return
    except ValueError:
        label_error.configure(text=config.LANGUAGES[current_lang]["error_text"])
        last_error_type = "length"
        clear_result_entry()
        return

    pool, pool_size = logic.get_pool_and_size(
        cb_letters_var.get(), 
        cb_digits_var.get(), 
        cb_symbols_var.get()
    )

    if not pool:
        label_error.configure(text=config.LANGUAGES[current_lang]["error_no_cb"])
        last_error_type = "no_cb"
        clear_result_entry()
        return

    password = logic.make_password(length, pool)
    
    entry_result.configure(state="normal")
    entry_result.delete(0, 'end')
    entry_result.insert(0, password)
    entry_result.configure(state="readonly")

    active_types = sum([cb_letters_var.get(), cb_digits_var.get(), cb_symbols_var.get()])
    progress, text, color = logic.check_strength(length, pool_size, active_types, current_lang)
    
    pbar_strength.set(progress)
    pbar_strength.configure(progress_color=color)
    lbl_strength.configure(text=text, text_color=color)

def copy_to_clipboard():
    password = entry_result.get()
    if password:
        app.clipboard_clear()
        app.clipboard_append(password)
        app.update()
        btn_copy.configure(text=config.LANGUAGES[current_lang]["copied"], fg_color="#4CAF50")

def show_about():
    about_win = ctk.CTkToplevel(app)
    about_win.title(config.LANGUAGES[current_lang]["about_title"])
    about_win.geometry("260x140")
    about_win.resizable(False, False)
    about_win.attributes("-topmost", True)

    about_win.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - (about_win.winfo_width() // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (about_win.winfo_height() // 2)
    about_win.geometry(f"+{x}+{y}")

    lbl = ctk.CTkLabel(about_win, text=config.LANGUAGES[current_lang]["about_text"], justify="center", font=("Arial", 12))
    lbl.pack(pady=(15, 5))

    lbl_link = ctk.CTkLabel(about_win, text="GitHub Releases", font=("Arial", 12, "underline"), text_color="#1F6AA5", cursor="hand2")
    lbl_link.pack(pady=5)
    lbl_link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(config.GITHUB_URL))

def switch_language():
    global current_lang, last_error_type
    current_lang = "en" if current_lang == "ru" else "ru"

    lang_dict = config.LANGUAGES[current_lang]

    app.title(lang_dict["title"])
    label_length.configure(text=lang_dict["length_lbl"])
    btn_generate.configure(text=lang_dict["btn_gen"])
    btn_about.configure(text=lang_dict["about_btn"])
    btn_lang.configure(text="RU" if current_lang == "ru" else "EN")
    cb_letters.configure(text=lang_dict["cb_letters"])
    cb_digits.configure(text=lang_dict["cb_digits"])
    cb_symbols.configure(text=lang_dict["cb_symbols"])
    btn_copy.configure(text=lang_dict["btn_copy"])

    if entry_result.get():
        try:
            length = int(entry_length.get())
            _, pool_size = logic.get_pool_and_size(cb_letters_var.get(), cb_digits_var.get(), cb_symbols_var.get())
            active_types = sum([cb_letters_var.get(), cb_digits_var.get(), cb_symbols_var.get()])
            
            progress, text, color = logic.check_strength(length, pool_size, active_types, current_lang)
            lbl_strength.configure(text=text, text_color=color)
            pbar_strength.set(progress)
        except ValueError:
            pass
    else:
        pbar_strength.set(0)
        lbl_strength.configure(text="")

    if last_error_type == "length":
        label_error.configure(text=lang_dict["error_text"])
    elif last_error_type == "no_cb":
        label_error.configure(text=lang_dict["error_no_cb"])

# ==================== СБОРКА ИНТЕРФЕЙСА ====================
app = ctk.CTk()
app.title(config.LANGUAGES[current_lang]["title"])
app.geometry("400x510")
app.resizable(False, False)

top_frame = ctk.CTkFrame(app, fg_color="transparent")
top_frame.pack(fill="x", padx=10, pady=10)

btn_lang = ctk.CTkButton(top_frame, text="RU", width=40, command=switch_language)
btn_lang.pack(side="left")

btn_about = ctk.CTkButton(top_frame, text=config.LANGUAGES[current_lang]["about_btn"], width=100, command=show_about)
btn_about.pack(side="right")

label_length = ctk.CTkLabel(app, text=config.LANGUAGES[current_lang]["length_lbl"], font=("Arial", 14))
label_length.pack(pady=(5, 5))

entry_length = ctk.CTkEntry(app, width=60, justify="center")
entry_length.insert(0, "12")
entry_length.pack(pady=5)

cb_frame = ctk.CTkFrame(app, fg_color="transparent")
cb_frame.pack(pady=10)

cb_letters_var = ctk.BooleanVar(value=True)
cb_letters = ctk.CTkCheckBox(cb_frame, text=config.LANGUAGES[current_lang]["cb_letters"], variable=cb_letters_var)
cb_letters.pack(anchor="w", pady=4)

cb_digits_var = ctk.BooleanVar(value=True)
cb_digits = ctk.CTkCheckBox(cb_frame, text=config.LANGUAGES[current_lang]["cb_digits"], variable=cb_digits_var)
cb_digits.pack(anchor="w", pady=4)

cb_symbols_var = ctk.BooleanVar(value=True)
cb_symbols = ctk.CTkCheckBox(cb_frame, text=config.LANGUAGES[current_lang]["cb_symbols"], variable=cb_symbols_var)
cb_symbols.pack(anchor="w", pady=4)

label_error = ctk.CTkLabel(app, text="", font=("Arial", 12, "bold"), text_color="#FF3B30")
label_error.pack(pady=2)

btn_generate = ctk.CTkButton(app, text=config.LANGUAGES[current_lang]["btn_gen"], font=("Arial", 14, "bold"), command=generate_password)
btn_generate.pack(pady=5)

entry_result = ctk.CTkEntry(app, width=280, justify="center", font=("Arial", 14), state="readonly")
entry_result.pack(pady=10)

lbl_strength = ctk.CTkLabel(app, text="", font=("Arial", 12, "bold"))
lbl_strength.pack(pady=(5, 2))

pbar_strength = ctk.CTkProgressBar(app, width=200, height=8, corner_radius=4)
pbar_strength.set(0)
pbar_strength.pack(pady=(0, 10))

btn_copy = ctk.CTkButton(app, text=config.LANGUAGES[current_lang]["btn_copy"], font=("Arial", 12), width=120, fg_color="#333333", command=copy_to_clipboard)
btn_copy.pack(pady=5)

default_copy_color = btn_copy.cget("fg_color")

app.mainloop()
