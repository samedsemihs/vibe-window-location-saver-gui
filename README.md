# Screen Location Saver

<div align="center">

![Windows](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)
![Python](https://img.shields.io/badge/Python-3.10+-green?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)

**[English](#english) | [Türkçe](#türkçe)**

</div>

---

## English

### About

Screen Location Saver is a Windows application that captures and restores window positions across multiple monitors. Perfect for users who frequently switch between monitor setups or want to quickly restore their workspace layout.

### Features

- **Save Window Layouts** - Capture positions of all open windows with one click
- **Restore Layouts** - Instantly restore windows to their saved positions
- **Multi-Monitor Support** - Works seamlessly with multiple monitor configurations
- **Auto-Start** - Optionally launch saved applications and restore layout on Windows startup
- **System Tray** - Runs quietly in the system tray, always accessible
- **Multiple Layouts** - Save and manage multiple named layouts
- **Bilingual UI** - English and Turkish language support

### Installation

1. Download the latest release or build from source
2. Run `install.bat`
3. Select your language (English or Turkish)
4. Done! The app will start automatically with Windows

**Install Location:** `%LOCALAPPDATA%\ScreenLocSaver\`

### Usage

| Action | Description |
|--------|-------------|
| **Save** | Enter a layout name and click "Save" to capture current window positions |
| **Restore** | Select a layout from the list and click "Restore" |
| **Delete** | Select a layout and click "Delete" to remove it |
| **System Tray** | Right-click the tray icon for quick access to Save/Show/Quit |

**Tip:** Save a layout named `default` - it will be automatically restored on Windows startup.

### Building from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run directly (development)
python main.py

# Build standalone executable
build.bat

# Install to system
install.bat

# Uninstall
uninstall.bat
```

### Requirements

- Windows 10/11
- Python 3.10+ (for building from source)

---

## Türkçe

### Hakkında

Screen Location Saver, çoklu monitör ortamlarında pencere konumlarını kaydedip geri yükleyen bir Windows uygulamasıdır. Monitör düzenleri arasında sık geçiş yapan veya çalışma alanı düzenini hızlıca geri yüklemek isteyen kullanıcılar için idealdir.

### Özellikler

- **Layout Kaydetme** - Tüm açık pencerelerin konumlarını tek tıkla kaydedin
- **Layout Geri Yükleme** - Pencereleri kaydedilmiş konumlarına anında geri yükleyin
- **Çoklu Monitör Desteği** - Birden fazla monitör yapılandırmasıyla sorunsuz çalışır
- **Otomatik Başlatma** - Windows açılışında uygulamaları başlatıp layout'u geri yükler
- **Sistem Tepsisi** - Sistem tepsisinde sessizce çalışır, her zaman erişilebilir
- **Çoklu Layout** - Birden fazla isimli layout kaydedin ve yönetin
- **İki Dil Desteği** - Türkçe ve İngilizce arayüz

### Kurulum

1. Son sürümü indirin veya kaynak koddan derleyin
2. `install.bat` dosyasını çalıştırın
3. Dilinizi seçin (Türkçe veya İngilizce)
4. Tamam! Uygulama Windows ile otomatik başlayacak

**Kurulum Konumu:** `%LOCALAPPDATA%\ScreenLocSaver\`

### Kullanım

| İşlem | Açıklama |
|-------|----------|
| **Kaydet** | Layout adı girin ve mevcut pencere konumlarını kaydetmek için "Kaydet"e tıklayın |
| **Geri Yükle** | Listeden bir layout seçin ve "Geri Yükle"ye tıklayın |
| **Sil** | Bir layout seçin ve kaldırmak için "Sil"e tıklayın |
| **Sistem Tepsisi** | Tepsi simgesine sağ tıklayarak Kaydet/Göster/Çıkış seçeneklerine hızlı erişin |

**İpucu:** `default` adında bir layout kaydedin - Windows açılışında otomatik olarak geri yüklenecektir.

### Kaynak Koddan Derleme

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Doğrudan çalıştır (geliştirme)
python main.py

# Bağımsız çalıştırılabilir dosya oluştur
build.bat

# Sisteme kur
install.bat

# Kaldır
uninstall.bat
```

### Gereksinimler

- Windows 10/11
- Python 3.10+ (kaynak koddan derlemek için)

---

## License / Lisans

MIT License - See [LICENSE](LICENSE) for details.

MIT Lisansı - Detaylar için [LICENSE](LICENSE) dosyasına bakın.
