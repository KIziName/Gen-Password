import random
import string
import math
import config

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
        return progress, lang_dict["strength_weak"], config.STRENGTH_COLORS["weak"]
    elif entropy < config.ENTROPY_MEDIUM_THRESHOLD:
        return progress, lang_dict["strength_medium"], config.STRENGTH_COLORS["medium"]
    else:
        return progress, lang_dict["strength_strong"], config.STRENGTH_COLORS["strong"]


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
    return "".join(random.choice(pool) for _ in range(length))