"""
EconRelayBot - Telegram Economic Channel Relay with optional AI Rewrite.
Single-file bot: monitors a source channel, cleans captions, posts to your channel.
"""

import os, re
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto

load_dotenv()

API_ID    = int(os.getenv("API_ID", "0"))
API_HASH  = os.getenv("API_HASH", "")
SOURCE    = os.getenv("SOURCE_CHANNEL", "")
TARGET    = os.getenv("TARGET_CHANNEL", "")
USE_PROXY = os.getenv("PROXY_ENABLED", "false").lower() == "true"
USE_LLM   = os.getenv("LLM_ENABLED", "false").lower() == "true"
LLM_KEY   = os.getenv("LLM_API_KEY", "")
LLM_URL   = os.getenv("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

proxy = None
if USE_PROXY:
    import socks
    ptype = {"SOCKS5": socks.SOCKS5, "SOCKS4": socks.SOCKS4, "HTTP": socks.HTTP}
    proxy = (
        ptype.get(os.getenv("PROXY_TYPE", "SOCKS5"), socks.SOCKS5),
        os.getenv("PROXY_HOST", "127.0.0.1"),
        int(os.getenv("PROXY_PORT", "1080")),
    )

client = TelegramClient("econ_session", API_ID, API_HASH, proxy=proxy)

PATTERNS = [r"@\w+", r"https?://t\.me/\S+", r"t\.me/\S+", r"https?://\S+"]

def clean(text):
    if not text:
        return ""
    for p in PATTERNS:
        text = re.sub(p, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

async def rewrite(text):
    if not text or not USE_LLM or not LLM_KEY:
        return text
    try:
        import httpx
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(LLM_URL, headers={
                "Authorization": f"Bearer {LLM_KEY}",
                "Content-Type": "application/json",
            }, json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content":
                        "Rewrite this economic news post. Remove all channel refs, "
                        "usernames, links, promotions. Keep facts accurate. "
                        "Preserve original language. Output only the rewritten text."},
                    {"role": "user", "content": text},
                ],
                "max_tokens": 1024, "temperature": 0.3,
            })
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return text

@client.on(events.NewMessage(chats=[SOURCE]))
async def handler(event):
    raw = event.message.message or ""
    caption = await rewrite(clean(raw)) if USE_LLM else clean(raw)

    if isinstance(event.message.media, MessageMediaPhoto):
        f = await event.message.download_media()
        await client.send_file(TARGET, f, caption=caption)
    elif caption:
        await client.send_message(TARGET, caption)
    print(f"[OK] msg {event.message.id}")

async def main():
    print(f"\n  EconRelayBot running")
    print(f"   {SOURCE}  ->  {TARGET}")
    print(f"   proxy={'on' if USE_PROXY else 'off'}  llm={'on' if USE_LLM else 'off'}\n")

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
