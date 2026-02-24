# EconRelayBot

Automated Telegram bot that monitors economic news channels, cleans captions, optionally rewrites them with AI, and posts to your own channel with images preserved and source references removed.

## Features

- **Real-time relay** - listens to source channel, instantly posts to yours
- **Caption cleaning** - strips @mentions, t.me links, URLs, promo text
- **AI rewrite** *(optional)* - plug any OpenAI-compatible API (OpenAI, Perplexity, Groq, Ollama)
- **Proxy support** - SOCKS5/HTTP for restricted regions (V2Ray, Shadowsocks)
- **Single file** - one main.py, easy to read, extend, and deploy

## Architecture

```
Source Channel -> Caption Cleaner (regex) -> LLM Rewriter (optional) -> Your Channel
```

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/econ-relay-bot.git
cd econ-relay-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env                  # fill in your values
python main.py             # first run: enter phone + code
```

## Configuration

All settings via .env - no hardcoded secrets.

| Variable | Required | Description |
|---|---|---|
| API_ID | Yes | Telegram API ID |
| API_HASH | Yes | Telegram API Hash |
| SOURCE_CHANNEL | Yes | Source channel to monitor |
| TARGET_CHANNEL | Yes | Your destination channel |
| PROXY_ENABLED | No | true to use SOCKS5/HTTP proxy |
| LLM_ENABLED | No | true to enable AI caption rewriting |
| LLM_API_KEY | No | API key for LLM provider |
| LLM_API_URL | No | OpenAI-compatible endpoint URL |
| LLM_MODEL | No | Model name (e.g. gpt-4o-mini) |

## Security

- .env and .session files are gitignored and never committed
- Session files equal your Telegram login so keep them private

## Roadmap

- [x] Real-time monitoring and relay
- [x] Regex caption cleaning
- [x] Proxy support
- [x] LLM rewrite module
- [ ] Multi-source channels
- [ ] Album/grouped media
- [ ] Docker deployment
- [ ] Message logging (SQLite)

## License

MIT
