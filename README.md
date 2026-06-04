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

Optional environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_POLL_INTERVAL` | `60` | Refresh interval in seconds |
| `CLAUDE_WORKING_DIR` | `~` | Directory for "Open Claude Code" menu item |

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

Необязательные переменные окружения:

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `CLAUDE_POLL_INTERVAL` | `60` | Интервал обновления в секундах |
| `CLAUDE_WORKING_DIR` | `~` | Директория для пункта меню "Open Claude Code" |

## License / Лицензия

MIT
