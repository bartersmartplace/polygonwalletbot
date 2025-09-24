from aiogram.utils.i18n import I18n
from pathlib import Path

I18N_DOMAIN = "messages"
LOCALES_DIR = Path(__file__).parent.parent / "localization" / "locales"
DEFAULT_LANGUAGE = "rus"

i18n = I18n(path=LOCALES_DIR, default_locale=DEFAULT_LANGUAGE, domain=I18N_DOMAIN)

_ = i18n.gettext
__ = i18n.lazy_gettext