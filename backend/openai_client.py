"""
Клиент OpenAI: чтение ключа из окружения, вызов chat completions (GPT-4).
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Модель по умолчанию (GPT-4o; для экономии можно заменить на gpt-4o-mini)
DEFAULT_MODEL = "gpt-4o"


def get_api_key() -> str | None:
    """Возвращает OPENAI_API_KEY из переменных окружения."""
    return os.environ.get("OPENAI_API_KEY")


def complete(system_prompt: str, user_content: str, model: str | None = None) -> str:
    """
    Вызов OpenAI Chat Completions.
    system_prompt — инструкция для модели, user_content — текст документа (или доп. контекст).
    Возвращает текст ответа ассистента.
    Выбрасывает ValueError, если ключ не задан; пробрасывает ошибки API.
    """
    api_key = get_api_key()
    if not api_key or not api_key.strip():
        raise ValueError(
            "OPENAI_API_KEY не задан. Создайте файл .env с OPENAI_API_KEY=ваш_ключ"
        )
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    model = model or DEFAULT_MODEL
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )
    message = response.choices[0].message
    if not message or not message.content:
        return ""
    return message.content.strip()
