from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_inline_markup(buttons_list: list[InlineKeyboardButton], row_length: int) -> InlineKeyboardMarkup:
    
    if len(buttons_list) == row_length == 0:
        return InlineKeyboardMarkup([])
    
    kb_list = [buttons_list[i:i + row_length] for i in range(0, len(buttons_list), row_length)]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)