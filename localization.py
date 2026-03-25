"""Localization strings for Screen Location Saver."""

STRINGS = {
    "tr": {
        # App window
        "app_title": "Screen Location Saver",
        "saved_layouts": "Kaydedilen Layout'lar:",
        "layout_name": "Layout Adı:",
        "btn_save": "✔ Kaydet",
        "btn_restore": "↺ Geri Yükle",
        "btn_delete": "✖ Sil",

        # Messages
        "warning": "Uyarı",
        "error": "Hata",
        "name_empty": "Layout adı boş olamaz.",
        "select_layout": "Bir layout seçin.",
        "layout_not_found": "'{name}' layout'u bulunamadı.",
        "restore_title": "Geri Yükleme",
        "restore_result": "{total} pencereden {matched} tanesi geri yüklendi.",
        "delete_confirm_title": "Silme Onayı",
        "delete_confirm": "'{name}' layout'unu silmek istediğinize emin misiniz?",

        # Feedback
        "saved": "✔  Kaydedildi!",

        # Tray menu
        "tray_show": "Göster",
        "tray_save": "Kaydet",
        "tray_quit": "Çıkış",
    },
    "en": {
        # App window
        "app_title": "Screen Location Saver",
        "saved_layouts": "Saved Layouts:",
        "layout_name": "Layout Name:",
        "btn_save": "✔ Save",
        "btn_restore": "↺ Restore",
        "btn_delete": "✖ Delete",

        # Messages
        "warning": "Warning",
        "error": "Error",
        "name_empty": "Layout name cannot be empty.",
        "select_layout": "Please select a layout.",
        "layout_not_found": "Layout '{name}' not found.",
        "restore_title": "Restore",
        "restore_result": "{matched} of {total} windows restored.",
        "delete_confirm_title": "Confirm Delete",
        "delete_confirm": "Are you sure you want to delete '{name}'?",

        # Feedback
        "saved": "✔  Saved!",

        # Tray menu
        "tray_show": "Show",
        "tray_save": "Save",
        "tray_quit": "Quit",
    },
}

_current_lang = "tr"


def set_language(lang: str):
    """Set the current language (tr or en)."""
    global _current_lang
    if lang in STRINGS:
        _current_lang = lang


def get_language() -> str:
    """Get the current language code."""
    return _current_lang


def t(key: str, **kwargs) -> str:
    """Get translated string by key, with optional formatting."""
    text = STRINGS.get(_current_lang, STRINGS["en"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text
