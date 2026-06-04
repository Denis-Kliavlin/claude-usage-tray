# Claude Usage Tray

**EN** | [RU](#ru)

Real-time Windows system tray monitor for [Claude](https://claude.ai) API usage limits.

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

Data is fetched from `claude.ai/api/organizations/{org}/usage` via [Chrome Bridge](https://nicedayzhu.github.io/chrome-bridge/) — a local browser automation tool that uses your active Claude session cookies.

## Features

- Tracks **5-hour session** and **7-day weekly** usage limits
- Tracks **extra usage credits** (used / monthly limit)
- **Toast notifications** at 70%, 80%, 90% thresholds
- **Notification on limit reset** when usage drops from 100%
- **Tooltip** with session / weekly / extra usage and reset countdown
- **Tray menu**: open Claude Desktop, open Claude Code CLI, manual refresh
- **Lock file** prevents duplicate instances
- Auto-refresh every 60 seconds (configurable)

## Requirements

- **Windows 10 / 11**
- **Python 3.10+**
- **[Chrome Bridge](https://nicedayzhu.github.io/chrome-bridge/)** running on `localhost:3456`
- Active Claude Pro/Team session in Chrome

### Install dependencies

```bash
pip install pystray Pillow winotify
```

## Setup

### 1. Get your Organization ID

1. Open [claude.ai/settings](https://claude.ai/settings) in Chrome
2. Copy the UUID from the URL: `claude.ai/settings/organizations/<THIS-IS-YOUR-ORG-ID>`

### 2. Set environment variable

```powershell
[Environment]::SetEnvironmentVariable("CLAUDE_ORG_ID", "your-org-id-here", "User")
```

### 3. Run

```bash
# Direct (with console)
python claude-usage-tray.py

# Hidden (no console window)
pythonw -X utf8 claude-usage-tray.py

# Via VBS launcher (recommended)
wscript start-claude-tray.vbs
```

### 4. Autostart (optional)

Place a shortcut to `start-claude-tray.vbs` in:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
```

## Configuration

All settings via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_ORG_ID` | *(required)* | Your Claude organization UUID |
| `CHROME_BRIDGE_URL` | `http://localhost:3456` | Chrome Bridge endpoint |
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

Данные получаются из `claude.ai/api/organizations/{org}/usage` через [Chrome Bridge](https://nicedayzhu.github.io/chrome-bridge/) — локальный инструмент автоматизации браузера, использующий куки активной сессии Claude.

## Возможности

- Отслеживание **5-часового сессионного** и **7-дневного недельного** лимитов
- Отслеживание **дополнительного расхода** (extra usage credits)
- **Уведомления** при достижении 70%, 80%, 90%
- **Уведомление о сбросе лимита** при снижении расхода со 100%
- **Тултип** с детальной информацией и обратным отсчётом до сброса
- **Меню в трее**: открыть Claude Desktop, Claude Code CLI, ручное обновление
- **Lock-файл** предотвращает запуск дублей
- Автообновление каждые 60 секунд (настраивается)

## Требования

- **Windows 10 / 11**
- **Python 3.10+**
- **[Chrome Bridge](https://nicedayzhu.github.io/chrome-bridge/)** запущен на `localhost:3456`
- Активная сессия Claude Pro/Team в Chrome

### Установка зависимостей

```bash
pip install pystray Pillow winotify
```

## Настройка

### 1. Получить Organization ID

1. Откройте [claude.ai/settings](https://claude.ai/settings) в Chrome
2. Скопируйте UUID из URL: `claude.ai/settings/organizations/<ВАШ-ORG-ID>`

### 2. Задать переменную окружения

```powershell
[Environment]::SetEnvironmentVariable("CLAUDE_ORG_ID", "ваш-org-id", "User")
```

### 3. Запуск

```bash
# С консолью
python claude-usage-tray.py

# Без консоли
pythonw -X utf8 claude-usage-tray.py

# Через VBS-лаунчер (рекомендуется)
wscript start-claude-tray.vbs
```

### 4. Автозагрузка (опционально)

Поместите ярлык на `start-claude-tray.vbs` в:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
```

## Конфигурация

Все настройки через переменные окружения:

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `CLAUDE_ORG_ID` | *(обязательно)* | UUID вашей организации Claude |
| `CHROME_BRIDGE_URL` | `http://localhost:3456` | Адрес Chrome Bridge |
| `CLAUDE_POLL_INTERVAL` | `60` | Интервал обновления в секундах |
| `CLAUDE_WORKING_DIR` | `~` | Директория для пункта меню "Open Claude Code" |

## License / Лицензия

MIT
