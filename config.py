# ----- Энтропия и стойкость -----
ENTROPY_WEAK_THRESHOLD = 42.0
ENTROPY_MEDIUM_THRESHOLD = 58.0
PENALTY_SINGLE_TYPE = 0.75
BONUS_MAX_DIVERSITY = 12.0
NORMALIZER = 75.0

# ----- Внешний вид -----
APPEARANCE_MODE = "System"       
COLOR_THEME = "blue"              

# ----- Размеры окна и отступы -----
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 540
PADX = 10
PADY = 10

# ----- Ограничения длины пароля -----
PASSWORD_MIN_LENGTH = 4
PASSWORD_MAX_LENGTH = 20
DEFAULT_LENGTH = 12

# ----- Состояние чекбоксов по умолчанию -----
DEFAULT_CHECKBOXES = {
    "letters": True,
    "digits": True,
    "symbols": True
}

# ----- Шрифты -----
FONT_FAMILY = "Arial"
FONT_SIZES = {
    "label": 14,
    "error": 12,
    "result": 14,
    "button": 14,
    "small": 12
}

# ----- Цвета для индикации стойкости -----
STRENGTH_COLORS = {
    "weak": "#FF3B30",
    "medium": "#FFCC00",
    "strong": "#4CAF50"
}

# ----- Прогресс-бар -----
PROGRESSBAR_WIDTH = 200
PROGRESSBAR_HEIGHT = 8
PROGRESSBAR_CORNER_RADIUS = 4

# ----- Окно "О программе" -----
ABOUT_WINDOW_WIDTH = 220
ABOUT_WINDOW_HEIGHT = 150

# ----- Ссылка на GitHub -----
GITHUB_URL = "https://github.com/KIziName/Gen-Password/releases"

# ----- Локализация -----
LANGUAGES = {
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
