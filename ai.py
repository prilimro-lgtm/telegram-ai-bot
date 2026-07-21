import aiohttp
from config import OPENROUTER_API_KEY, MODEL

URL = "https://openrouter.ai/api/v1/chat/completions"

async def ask_ai(history, message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []

    if history:
        messages.append({
            "role": "system",
            "content": history
        })

    messages.append({
        "role": "user",
        "content": message
    })

    payload = {
        "model": MODEL,
        "messages": messages
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, headers=headers, json=payload) as response:
            data = await response.json()

            if "choices" not in data:
                return "Ошибка при обращении к ИИ."

            return data["choices"][0]["message"]["content"]
