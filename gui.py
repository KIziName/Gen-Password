import customtkinter as ctk
import webbrowser
import config
import logic

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.current_lang = "ru"
        self.last_error_type = None

        # Настройки темы
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # === Сборка интерфейса ===
        self.title(config.LANGUAGES[self.current_lang]["title"])
        self.geometry("400x510")
        self.resizable(False, False)

        # Верхняя панель
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        self.btn_lang = ctk.CTkButton(top_frame, text="RU", width=40, command=self.switch_language)
        self.btn_lang.pack(side="left")

        self.btn_about = ctk.CTkButton(top_frame, text=config.LANGUAGES[self.current_lang]["about_btn"], width=100, command=self.show_about)
        self.btn_about.pack(side="right")

        # Длина пароля
        self.label_length = ctk.CTkLabel(self, text=config.LANGUAGES[self.current_lang]["length_lbl"], font=("Arial", 14))
        self.label_length.pack(pady=(5, 5))

        self.entry_length = ctk.CTkEntry(self, width=60, justify="center")
        self.entry_length.insert(0, "12")
        self.entry_length.pack(pady=5)

        # Чекбоксы
        cb_frame = ctk.CTkFrame(self, fg_color="transparent")
        cb_frame.pack(pady=10)

        self.cb_letters_var = ctk.BooleanVar(value=True)
        self.cb_letters = ctk.CTkCheckBox(cb_frame, text=config.LANGUAGES[self.current_lang]["cb_letters"], variable=self.cb_letters_var)
        self.cb_letters.pack(anchor="w", pady=4)

        self.cb_digits_var = ctk.BooleanVar(value=True)
        self.cb_digits = ctk.CTkCheckBox(cb_frame, text=config.LANGUAGES[self.current_lang]["cb_digits"], variable=self.cb_digits_var)
        self.cb_digits.pack(anchor="w", pady=4)

        self.cb_symbols_var = ctk.BooleanVar(value=True)
        self.cb_symbols = ctk.CTkCheckBox(cb_frame, text=config.LANGUAGES[self.current_lang]["cb_symbols"], variable=self.cb_symbols_var)
        self.cb_symbols.pack(anchor="w", pady=4)

        # Ошибка
        self.label_error = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"), text_color="#FF3B30")
        self.label_error.pack(pady=2)

        # Кнопка генерации
        self.btn_generate = ctk.CTkButton(self, text=config.LANGUAGES[self.current_lang]["btn_gen"], font=("Arial", 14, "bold"), command=self.generate_password)
        self.btn_generate.pack(pady=5)

        # Поле результата
        self.entry_result = ctk.CTkEntry(self, width=280, justify="center", font=("Arial", 14), state="readonly")
        self.entry_result.pack(pady=10)

        # Метка стойкости
        self.lbl_strength = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"))
        self.lbl_strength.pack(pady=(5, 2))

        # Прогресс-бар стойкости
        self.pbar_strength = ctk.CTkProgressBar(self, width=200, height=8, corner_radius=4)
        self.pbar_strength.set(0)
        self.pbar_strength.pack(pady=(0, 10))

        # Кнопка копирования
        self.btn_copy = ctk.CTkButton(self, text=config.LANGUAGES[self.current_lang]["btn_copy"], font=("Arial", 12), width=120, fg_color="#333333", command=self.copy_to_clipboard)
        self.btn_copy.pack(pady=5)

        self.default_copy_color = self.btn_copy.cget("fg_color")

    # === Методы ===
    def clear_result_entry(self):
        self.entry_result.configure(state="normal")
        self.entry_result.delete(0, 'end')
        self.entry_result.configure(state="readonly")

    def generate_password(self):
        self.label_error.configure(text="")
        self.last_error_type = None
        self.btn_copy.configure(text=config.LANGUAGES[self.current_lang]["btn_copy"], fg_color=self.default_copy_color)

        self.pbar_strength.set(0)
        self.lbl_strength.configure(text="", text_color="white")

        try:
            length = int(self.entry_length.get())
            if length < 4 or length > 20:
                self.label_error.configure(text=config.LANGUAGES[self.current_lang]["error_text"])
                self.last_error_type = "length"
                self.clear_result_entry()
                return
        except ValueError:
            self.label_error.configure(text=config.LANGUAGES[self.current_lang]["error_text"])
            self.last_error_type = "length"
            self.clear_result_entry()
            return

        pool, pool_size = logic.get_pool_and_size(
            self.cb_letters_var.get(),
            self.cb_digits_var.get(),
            self.cb_symbols_var.get()
        )

        if not pool:
            self.label_error.configure(text=config.LANGUAGES[self.current_lang]["error_no_cb"])
            self.last_error_type = "no_cb"
            self.clear_result_entry()
            return

        password = logic.make_password(length, pool)

        self.entry_result.configure(state="normal")
        self.entry_result.delete(0, 'end')
        self.entry_result.insert(0, password)
        self.entry_result.configure(state="readonly")

        active_types = sum([self.cb_letters_var.get(), self.cb_digits_var.get(), self.cb_symbols_var.get()])
        progress, text, color = logic.check_strength(length, pool_size, active_types, self.current_lang)

        self.pbar_strength.set(progress)
        self.pbar_strength.configure(progress_color=color)
        self.lbl_strength.configure(text=text, text_color=color)

    def copy_to_clipboard(self):
        password = self.entry_result.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update()
            self.btn_copy.configure(text=config.LANGUAGES[self.current_lang]["copied"], fg_color="#4CAF50")

    def show_about(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title(config.LANGUAGES[self.current_lang]["about_title"])
        about_win.geometry("260x140")
        about_win.resizable(False, False)
        about_win.attributes("-topmost", True)

        about_win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (about_win.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (about_win.winfo_height() // 2)
        about_win.geometry(f"+{x}+{y}")

        lbl = ctk.CTkLabel(about_win, text=config.LANGUAGES[self.current_lang]["about_text"], justify="center", font=("Arial", 12))
        lbl.pack(pady=(15, 5))

        lbl_link = ctk.CTkLabel(about_win, text="GitHub Releases", font=("Arial", 12, "underline"), text_color="#1F6AA5", cursor="hand2")
        lbl_link.pack(pady=5)
        lbl_link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(config.GITHUB_URL))

    def switch_language(self):
        self.current_lang = "en" if self.current_lang == "ru" else "ru"
        lang_dict = config.LANGUAGES[self.current_lang]

        self.title(lang_dict["title"])
        self.label_length.configure(text=lang_dict["length_lbl"])
        self.btn_generate.configure(text=lang_dict["btn_gen"])
        self.btn_about.configure(text=lang_dict["about_btn"])
        self.btn_lang.configure(text="RU" if self.current_lang == "ru" else "EN")
        self.cb_letters.configure(text=lang_dict["cb_letters"])
        self.cb_digits.configure(text=lang_dict["cb_digits"])
        self.cb_symbols.configure(text=lang_dict["cb_symbols"])
        self.btn_copy.configure(text=lang_dict["btn_copy"])

        if self.entry_result.get():
            try:
                length = int(self.entry_length.get())
                _, pool_size = logic.get_pool_and_size(
                    self.cb_letters_var.get(),
                    self.cb_digits_var.get(),
                    self.cb_symbols_var.get()
                )
                active_types = sum([self.cb_letters_var.get(), self.cb_digits_var.get(), self.cb_symbols_var.get()])
                progress, text, color = logic.check_strength(length, pool_size, active_types, self.current_lang)
                self.lbl_strength.configure(text=text, text_color=color)
                self.pbar_strength.set(progress)
            except ValueError:
                pass
        else:
            self.pbar_strength.set(0)
            self.lbl_strength.configure(text="")

        if self.last_error_type == "length":
            self.label_error.configure(text=lang_dict["error_text"])
        elif self.last_error_type == "no_cb":
            self.label_error.configure(text=lang_dict["error_no_cb"])
