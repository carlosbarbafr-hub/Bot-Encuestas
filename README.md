# Bot-Encuestas

Discord bot for automated weekly availability polls with scheduling and reminder system for RPG communities.

## Features

- Weekly poll every Sunday at 17:00 (UTC+2) asking "¿Qué días puedes jugar?" with multi-select for all 7 days
- Reminder messages on Tuesday, Friday, and Sunday at 16:59
- Manual `!encuesta` command to trigger the poll anytime
- `!ping` health check command

## Tech Stack

- Python 3.13
- discord.py 2.7.1
- Railway (hosting)

## Development

```bash
pip install -r requirements.txt
python bot.py
```

> **Note:** This repo is mirrored from [carlosbarbafr-hub/Bot-Encuestas](https://github.com/carlosbarbafr-hub/Bot-Encuestas) — the original is hosted on that account.
