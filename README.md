# 📡 EconRelayBot

Single-file Telegram relay bot. It listens to one chat (channel or group), cleans the caption text, optionally rewrites it with an AI model, and reposts it to another chat. Images are preserved; source references and links can be removed.

I mainly use it for economic / financial news, but it works for **any topic** and any chat you can access.

---

## ✨ Features

- **Any chat → any chat**  
  Source and target can be channels, supergroups, or private chats (`@username` or numeric ID).

- **Caption cleaning**  
  Removes `@mentions`, `t.me` links, and other URLs before posting to your own chat.

- **Optional AI rewrite**  
  If you provide an OpenAI‑compatible API key (OpenAI, Perplexity, Groq, Ollama, etc.), the bot can rewrite captions in a cleaner, professional style.

- **Proxy support**  
  Built‑in SOCKS5 / HTTP proxy configuration for regions where Telegram is blocked (e.g. local V2Ray).

- **Simple code**  
  One `main.py` plus `.env` configuration; easy to read, fork, and extend.

---

## 🏗 Architecture

```text
Source chat (channel/group)
    │  new message
    ▼
Caption cleaner (regex)
    │  cleaned text
    ▼
LLM rewriter (optional, OpenAI‑compatible)
    │  final caption
    ▼
Target chat (channel/group)