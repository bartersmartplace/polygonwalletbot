from tg_bot.localization import _


class AdminPresenter:
    def __init__(self, language: str = "en"):
        self._ = lambda text: _(text, locale=language)


    def get_admin_menu_message(self):
        return self._("Choose option:")


    def get_user_count_message(self, user_count: int) -> str:
        return self._("Total user count: {user_count}").format(user_count=user_count)

    def ask_english_message_entering(self):
        return self._("Send the text for the mailing list in English")


    def ask_russian_message_entering(self):
        return self._("Send the text for the mailing list in Russian")
    

    def ask_english_buttons_entering(self):
        return self._("Send the URL buttons for the English message in the following format:\n" + \
                      "buttons 1 - http://example1.com\n" + \
                      "buttons 2 - http://example2.com\n\n")


    def ask_russian_buttons_entering(self):
        return self._("Send the URL buttons for the Russian message in the following format:\n" + \
                      "buttons 1 - http://example1.com\n" + \
                      "buttons 2 - http://example2.com\n\n")


    def get_admin_message_preview(self):
        return self._("Examples of the messages presented above.")
    

    def get_broadcast_summary_message(self, successful_message_count):
        return self._(
            "The message broadcasting is completed\n\n" + \
            "Messages have been sent to {successful_message_count} users"
            ).format(successful_message_count=successful_message_count)