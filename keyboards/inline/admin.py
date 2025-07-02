from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def key_returner(current_page, all_pages):
    keys = InlineKeyboardMarkup(row_width=3)
    keys.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_stat:{current_page}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_stat:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_stat:{current_page}"
        )
    )
    return keys
