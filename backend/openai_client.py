"""
Клиент LLM через OpenRouter: чтение ключа из окружения, вызов chat completions.
OpenRouter — единый API для разных моделей (OpenAI, Anthropic и др.).
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Base URL OpenRouter (OpenAI-совместимый API)
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Модель по умолчанию (через OpenRouter: openai/gpt-4o или openai/gpt-4o-mini)
DEFAULT_MODEL = "openai/gpt-4o"

# Лимит токенов ответа (укладываемся в бесплатный лимит OpenRouter; при 402 — уменьшить)
MAX_TOKENS = 1200


def get_api_key() -> str | None:
    """Возвращает OPENROUTER_API_KEY из переменных окружения."""
    return os.environ.get("OPENROUTER_API_KEY")


def complete(system_prompt: str, user_content: str, model: str | None = None) -> str:
    """
    Вызов Chat Completions через OpenRouter (OpenAI-совместимый API).
    system_prompt — инструкция для модели, user_content — текст документа.
    Возвращает текст ответа ассистента.
    Выбрасывает ValueError, если ключ не задан; пробрасывает ошибки API.
    """
    api_key = get_api_key()
    if not api_key or not api_key.strip():
        raise ValueError(
            "OPENROUTER_API_KEY не задан. Создайте файл .env с OPENROUTER_API_KEY=ваш_ключ"
        )
    from openai import OpenAI

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
    model = model or DEFAULT_MODEL
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        max_tokens=MAX_TOKENS,
    )
    message = response.choices[0].message
    if not message or not message.content:
        return ""
    return message.content.strip()
