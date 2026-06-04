# Claude Usage Tray

**EN** | [RU](#ru)

Real-time Windows system tray monitor for [Claude](https://claude.ai) usage limits.

![Windows](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## How it works

The app sits in your system tray and shows your current Claude usage as a color-coded percentage icon:

| Color | Usage |
|-------|-------|
| Green | < 50% |
| Yellow | 50 - 70% |
| Orange | 70 - 85% |
| Red | > 85% |

Uses **Claude Code OAuth credentials** (`~/.claude/.credentials.json`) to fetch usage data directly from `api.anthropic.com`. No browser automation, no cookies, no extra tools needed.

## Features

- Tracks **5-hour session** and **7-day weekly** usage limits
- Tracks **extra usage credits** (used / monthly limit)
- **Toast notifications** at 70%, 80%, 90% thresholds
- **Notification on limit reset** when usage drops from 100%
- **Tooltip** with session / weekly / extra usage and reset countdown
- **Tray menu**: open Claude Desktop, open Claude Code CLI, manual refresh
- **Auto token refresh** when OAuth token expires
- **Lock file** prevents duplicate instances
- Auto-refresh every 60 seconds (configurable)

## Prerequisites

- **Windows 10 / 11**
- **Python 3.10+**
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** installed and logged in (`claude` CLI)

### Install dependencies

```bash
pip install pystray Pillow winotify
```

## Setup

### 1. Make sure Claude Code is logged in

```bash
claude
```

This creates `~/.claude/.credentials.json` with OAuth tokens. That's all the app needs.

### 2. Run

```bash
# Direct (with console)
python claude-usage-tray.py

# Hidden (no console window)
pythonw -X utf8 claude-usage-tray.py

# Via VBS launcher (recommended)
wscript start-claude-tray.vbs
```

### 3. Autostart (optional)

Place a shortcut to `start-claude-tray.vbs` in:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
```

## Configuration

On first run, `config.json` is created next to the script with default values. Edit it to customize:

```json
{
  "poll_interval": 60,
  "thresholds": [70, 80, 90],
  "icon_size": 64,
  "credentials_path": "C:\\Users\\you\\.claude\\.credentials.json",
  "working_dir": "C:\\Users\\you",
  "notification_sound": true,
  "notify_on_reset": true,
  "colors": {
    "green": [76, 175, 80],
    "yellow": [255, 193, 7],
    "orange": [255, 152, 0],
    "red": [244, 67, 54]
  },
  "color_thresholds": [50, 70, 85]
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `poll_interval` | `60` | Refresh interval in seconds |
| `thresholds` | `[70, 80, 90]` | Usage % levels that trigger notifications |
| `icon_size` | `64` | Tray icon size in pixels |
| `credentials_path` | `~/.claude/.credentials.json` | Path to Claude Code OAuth credentials |
| `working_dir` | `~` | Directory for "Open Claude Code" menu item |
| `notification_sound` | `true` | Play sound with toast notifications |
| `notify_on_reset` | `true` | Notify when limits refresh (100% -> lower) |
| `colors` | green/yellow/orange/red | RGB colors for each usage level |
| `color_thresholds` | `[50, 70, 85]` | Usage % breakpoints for color changes |

---

<a id="ru"></a>

# Claude Usage Tray (RU)

**[EN](#claude-usage-tray)** | RU

Монитор расхода лимитов [Claude](https://claude.ai) в системном трее Windows.

## Как это работает

Приложение отображает текущий расход лимитов Claude в виде цветной иконки с процентами в системном трее:

| Цвет | Расход |
|------|--------|
| Зелёный | < 50% |
| Жёлтый | 50 - 70% |
| Оранжевый | 70 - 85% |
| Красный | > 85% |

Использует **OAuth-токены Claude Code** (`~/.claude/.credentials.json`) для получения данных напрямую с `api.anthropic.com`. Никакой автоматизации браузера, куки или дополнительных инструментов не требуется.

## Возможности

- Отслеживание **5-часового сессионного** и **7-дневного недельного** лимитов
- Отслеживание **дополнительного расхода** (extra usage credits)
- **Уведомления** при достижении 70%, 80%, 90%
- **Уведомление о сбросе лимита** при снижении расхода со 100%
- **Тултип** с детальной информацией и обратным отсчётом до сброса
- **Меню в трее**: открыть Claude Desktop, Claude Code CLI, ручное обновление
- **Автоматическое обновление токена** при истечении OAuth
- **Lock-файл** предотвращает запуск дублей
- Автообновление каждые 60 секунд (настраивается)

## Требования

- **Windows 10 / 11**
- **Python 3.10+**
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** установлен и залогинен (CLI `claude`)

### Установка зависимостей

```bash
pip install pystray Pillow winotify
```

## Настройка

### 1. Убедитесь что Claude Code залогинен

```bash
claude
```

Это создаёт `~/.claude/.credentials.json` с OAuth-токенами. Это всё что нужно приложению.

### 2. Запуск

```bash
# С консолью
python claude-usage-tray.py

# Без консоли
pythonw -X utf8 claude-usage-tray.py

# Через VBS-лаунчер (рекомендуется)
wscript start-claude-tray.vbs
```

### 3. Автозагрузка (опционально)

Поместите ярлык на `start-claude-tray.vbs` в:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
```

## Конфигурация

При первом запуске рядом со скриптом создаётся `config.json` с настройками по умолчанию. Отредактируйте его:

```json
{
  "poll_interval": 60,
  "thresholds": [70, 80, 90],
  "icon_size": 64,
  "credentials_path": "C:\\Users\\you\\.claude\\.credentials.json",
  "working_dir": "C:\\Users\\you",
  "notification_sound": true,
  "notify_on_reset": true,
  "colors": {
    "green": [76, 175, 80],
    "yellow": [255, 193, 7],
    "orange": [255, 152, 0],
    "red": [244, 67, 54]
  },
  "color_thresholds": [50, 70, 85]
}
```

| Параметр | По умолчанию | Описание |
|----------|--------------|----------|
| `poll_interval` | `60` | Интервал обновления в секундах |
| `thresholds` | `[70, 80, 90]` | Пороги % для уведомлений |
| `icon_size` | `64` | Размер иконки в трее |
| `credentials_path` | `~/.claude/.credentials.json` | Путь к OAuth-токенам Claude Code |
| `working_dir` | `~` | Директория для пункта меню "Open Claude Code" |
| `notification_sound` | `true` | Звук при уведомлениях |
| `notify_on_reset` | `true` | Уведомлять при сбросе лимита (100% -> ниже) |
| `colors` | green/yellow/orange/red | RGB-цвета для каждого уровня расхода |
| `color_thresholds` | `[50, 70, 85]` | Пороги % для смены цвета иконки |

## License / Лицензия

MIT
