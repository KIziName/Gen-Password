import sys
import ctypes
import atexit
import os
import random
import string
import math
import config

def init_system_wide_mutex():
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

def check_strength(length, pool_size, active_types, lang):
    if pool_size == 0 or length == 0:
        return 0.0, "", "#333333"

    entropy = length * math.log2(pool_size)
    lang_dict = config.LANGUAGES[lang]

    if active_types == 1:
        entropy *= config.PENALTY_SINGLE_TYPE
    elif active_types == 3 and length >= 8:
        entropy += config.BONUS_MAX_DIVERSITY

    progress = min(entropy / config.NORMALIZER, 1.0)

    if entropy < config.ENTROPY_WEAK_THRESHOLD:
        return progress, lang_dict["strength_weak"], "#FF3B30"
    elif entropy < config.ENTROPY_MEDIUM_THRESHOLD:
        return progress, lang_dict["strength_medium"], "#FFCC00"
    else:
        return progress, lang_dict["strength_strong"], "#4CAF50"

def get_pool_and_size(use_letters, use_digits, use_symbols):
    pool = ""
    pool_size = 0
    if use_letters:
        pool += string.ascii_letters
        pool_size += 52
    if use_digits:
        pool += string.digits
        pool_size += 10
    if use_symbols:
        pool += string.punctuation
        pool_size += len(string.punctuation)
    return pool, pool_size

def make_password(length, pool):
    return ''.join(random.choice(pool) for _ in range(length))
