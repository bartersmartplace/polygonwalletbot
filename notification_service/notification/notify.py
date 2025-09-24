from aiogram.utils.markdown import hlink
from notification_service.dto import Deposit
from tg_bot.bot_instance import bot


def get_notification_message(
          language: str,
          deposit_amount: int,
          deposit_currency_symbol: str,
          deposit_address: str,
          tx_hash_url: str
          ):
    
    if language == "rus":
        message = f"Вы получили {str(deposit_amount)} {deposit_currency_symbol} на адрес {deposit_address}\n" + \
                  f"{hlink('Хэш транзакции', tx_hash_url)}"
    else:
        message = f"You received {str(deposit_amount)} {deposit_currency_symbol} at address: {deposit_address}\n" + \
                  f"{hlink('Transaction hash', tx_hash_url)}"
    return message


async def notify_about_deposits(deposits: list[Deposit]):
    if not deposits:
        return
    
    for deposit in deposits:
        tx_hash_url = f"https://polygonscan.com/tx/{deposit.hash}"
        message = get_notification_message(
            deposit.language,
            str(deposit.amount),
            deposit.currency_symbol,
            deposit.address, tx_hash_url)
        await send_notification(str(message), [deposit.telegram_id])


async def send_notification(message: str, user_list: list[int]):
    """
    Sends a message to list of users
    """
    for user_id in user_list:
        try:
            await bot.send_message(user_id, message,  parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
                if str(e) == "Telegram server says - Forbidden: bot was blocked by the user":
                    print(str(e))
                else:
                     print(str(e))