import webbrowser
import customtkinter as ctk
import config
import logic

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "ru"
        self.last_error_type = None

        ctk.set_appearance_mode(config.APPEARANCE_MODE)
        ctk.set_default_color_theme(config.COLOR_THEME)

        self.title(config.LANGUAGES[self.current_lang]["title"])
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.resizable(False, False)

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=config.PADX, pady=config.PADY)

        self.btn_lang = ctk.CTkButton(
            top_frame, text="RU", width=40, command=self.switch_language
        )
        self.btn_lang.pack(side="left")

        self.btn_about = ctk.CTkButton(
            top_frame,
            text=config.LANGUAGES[self.current_lang]["about_btn"],
            width=100,
            command=self.show_about,
        )
        self.btn_about.pack(side="right")

        self.label_length = ctk.CTkLabel(
            self,
            text=config.LANGUAGES[self.current_lang]["length_lbl"],
            font=(config.FONT_FAMILY, config.FONT_SIZES["label"]),
        )
        self.label_length.pack(pady=(5, 5))

        self.entry_length = ctk.CTkEntry(self, width=60, justify="center")
        self.entry_length.insert(0, str(config.DEFAULT_LENGTH))
        self.entry_length.pack(pady=5)

        cb_frame = ctk.CTkFrame(self, fg_color="transparent")
        cb_frame.pack(pady=config.PADY)

        self.cb_letters_var = ctk.BooleanVar(value=config.DEFAULT_CHECKBOXES["letters"])
        self.cb_letters = ctk.CTkCheckBox(
            cb_frame,
            text=config.LANGUAGES[self.current_lang]["cb_letters"],
            variable=self.cb_letters_var,
        )
        self.cb_letters.pack(anchor="w", pady=4)

        self.cb_digits_var = ctk.BooleanVar(value=config.DEFAULT_CHECKBOXES["digits"])
        self.cb_digits = ctk.CTkCheckBox(
            cb_frame,
            text=config.LANGUAGES[self.current_lang]["cb_digits"],
            variable=self.cb_digits_var,
        )
        self.cb_digits.pack(anchor="w", pady=4)

        self.cb_symbols_var = ctk.BooleanVar(value=config.DEFAULT_CHECKBOXES["symbols"])
        self.cb_symbols = ctk.CTkCheckBox(
            cb_frame,
            text=config.LANGUAGES[self.current_lang]["cb_symbols"],
            variable=self.cb_symbols_var,
        )
        self.cb_symbols.pack(anchor="w", pady=4)

        self.label_error = ctk.CTkLabel(
            self,
            text="",
            font=(config.FONT_FAMILY, config.FONT_SIZES["error"], "bold"),
            text_color="#FF3B30",  # цвет ошибки пока оставлен жёстко
        )
        self.label_error.pack(pady=2)

        self.btn_generate = ctk.CTkButton(
            self,
            text=config.LANGUAGES[self.current_lang]["btn_gen"],
            font=(config.FONT_FAMILY, config.FONT_SIZES["button"], "bold"),
            command=self.generate_password,
        )
        self.btn_generate.pack(pady=5)

        self.entry_result = ctk.CTkEntry(
            self,
            width=280,
            justify="center",
            font=(config.FONT_FAMILY, config.FONT_SIZES["result"]),
            state="readonly",
        )
        self.entry_result.pack(pady=config.PADY)
        
        self.lbl_strength = ctk.CTkLabel(
            self,
            text="",
            font=(config.FONT_FAMILY, config.FONT_SIZES["small"], "bold"),
        )
        self.lbl_strength.pack(pady=(5, 2))

        self.pbar_strength = ctk.CTkProgressBar(
            self,
            width=config.PROGRESSBAR_WIDTH,
            height=config.PROGRESSBAR_HEIGHT,
            corner_radius=config.PROGRESSBAR_CORNER_RADIUS,
        )
        self.pbar_strength.set(0)
        self.pbar_strength.pack(pady=(0, config.PADY))

        self.btn_copy = ctk.CTkButton(
            self,
            text=config.LANGUAGES[self.current_lang]["btn_copy"],
            font=(config.FONT_FAMILY, config.FONT_SIZES["small"]),
            width=120,
            fg_color="#333333",
            command=self.copy_to_clipboard,
        )
        self.btn_copy.pack(pady=5)

        self.default_copy_color = self.btn_copy.cget("fg_color")

    def clear_result_entry(self):
        self.entry_result.configure(state="normal")
        self.entry_result.delete(0, "end")
        self.entry_result.configure(state="readonly")

    def generate_password(self):
        self.label_error.configure(text="")
        self.last_error_type = None
        self.btn_copy.configure(
            text=config.LANGUAGES[self.current_lang]["btn_copy"],
            fg_color=self.default_copy_color,
        )

        self.pbar_strength.set(0)
        self.lbl_strength.configure(text="", text_color="white")

        try:
            length = int(self.entry_length.get())
            if length < config.PASSWORD_MIN_LENGTH or length > config.PASSWORD_MAX_LENGTH:
                self.label_error.configure(
                    text=config.LANGUAGES[self.current_lang]["error_text"]
                )
                self.last_error_type = "length"
                self.clear_result_entry()
                return
        except ValueError:
            self.label_error.configure(
                text=config.LANGUAGES[self.current_lang]["error_text"]
            )
            self.last_error_type = "length"
            self.clear_result_entry()
            return

        pool, pool_size = logic.get_pool_and_size(
            self.cb_letters_var.get(),
            self.cb_digits_var.get(),
            self.cb_symbols_var.get(),
        )

        if not pool:
            self.label_error.configure(
                text=config.LANGUAGES[self.current_lang]["error_no_cb"]
            )
            self.last_error_type = "no_cb"
            self.clear_result_entry()
            return

        password = logic.make_password(length, pool)

        self.entry_result.configure(state="normal")
        self.entry_result.delete(0, "end")
        self.entry_result.insert(0, password)
        self.entry_result.configure(state="readonly")

        active_types = sum(
            [
                self.cb_letters_var.get(),
                self.cb_digits_var.get(),
                self.cb_symbols_var.get(),
            ]
        )
        progress, text, color = logic.check_strength(
            length, pool_size, active_types, self.current_lang
        )

        self.pbar_strength.set(progress)
        self.pbar_strength.configure(progress_color=color)
        self.lbl_strength.configure(text=text, text_color=color)

    def copy_to_clipboard(self):
        password = self.entry_result.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update()
            self.btn_copy.configure(
                text=config.LANGUAGES[self.current_lang]["copied"],
                fg_color=config.STRENGTH_COLORS["strong"],  # #4CAF50
            )

    def show_about(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title(config.LANGUAGES[self.current_lang]["about_title"])
        about_win.geometry(
            f"{config.ABOUT_WINDOW_WIDTH}x{config.ABOUT_WINDOW_HEIGHT}"
        )
        about_win.resizable(False, False)
        about_win.attributes("-topmost", True)

        about_win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (about_win.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (about_win.winfo_height() // 2)
        about_win.geometry(f"+{x}+{y}")

        lbl = ctk.CTkLabel(
            about_win,
            text=config.LANGUAGES[self.current_lang]["about_text"],
            justify="center",
            font=(config.FONT_FAMILY, config.FONT_SIZES["small"]),
        )
        lbl.pack(pady=(15, 5))

        lbl_link = ctk.CTkLabel(
            about_win,
            text="GitHub Releases",
            font=(config.FONT_FAMILY, config.FONT_SIZES["small"], "underline"),
            text_color="#1F6AA5",
            cursor="hand2",
        )
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
                    self.cb_symbols_var.get(),
                )
                active_types = sum(
                    [
                        self.cb_letters_var.get(),
                        self.cb_digits_var.get(),
                        self.cb_symbols_var.get(),
                    ]
                )
                progress, text, color = logic.check_strength(
                    length, pool_size, active_types, self.current_lang
                )
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
