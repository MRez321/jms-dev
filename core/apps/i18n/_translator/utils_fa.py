import os
from typing import Protocol

from openai import AsyncOpenAI


class Translator(Protocol):
    async def translate_text(
            self,
            text: str,
            target_lang: str = "Persian",
    ) -> str | None:
        ...


_TRANSLATION_SYSTEM_PROMPT = """
You are a professional software localization translator.

Translate all Chinese text into modern standard Persian (Farsi).

Rules:

- Return ONLY the translated text.
- Do NOT add explanations.
- Do NOT add notes.
- Do NOT change formatting.
- Preserve line breaks exactly.
- Preserve whitespace exactly.
- Preserve punctuation unless Persian typography requires it.
- Keep UI text concise and natural.
- Use terminology appropriate for software and user interfaces.

DO NOT translate or modify:

%s
%d
%(name)s
{name}
{}
{{value}}
<tag>...</tag>
HTML tags
XML tags
Markdown
URLs
Email addresses
Variables
Escape sequences
File paths

If the Chinese word "动作" appears, translate it as "Action".

If the Chinese word "管理" is used as a menu title, leave it unchanged.

Return ONLY the Persian translation.
"""


class OpenAITranslate:
    def __init__(
            self,
            key: str | None = None,
            base_url: str | None = None,
            model: str | None = None,
    ):
        key = key or os.getenv("OPENAI_API_KEY")

        base_url = (
                base_url
                or os.getenv("OPENAI_BASE_URL")
                or None
        )

        self.model = (
                model
                or os.getenv("OPENAI_MODEL")
                or "openai/gpt-4.1-mini"
        )

        self.client = AsyncOpenAI(
            api_key=key,
            base_url=base_url,
        )

    async def translate_text(
            self,
            text: str,
            target_lang: str = "Persian",
    ) -> str | None:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                max_tokens=2048,
                messages=[
                    {
                        "role": "system",
                        "content": _TRANSLATION_SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print("OpenAI Error:", e)
            return None


class ClaudeTranslate:
    def __init__(
            self,
            key: str | None = None,
            model: str | None = None,
    ):
        from anthropic import AsyncAnthropic

        key = key or os.getenv("ANTHROPIC_API_KEY")

        self.model = (
                model
                or os.getenv("ANTHROPIC_MODEL")
                or "claude-3-5-sonnet-latest"
        )

        self.client = AsyncAnthropic(api_key=key)

    async def translate_text(
            self,
            text: str,
            target_lang: str = "Persian",
    ) -> str | None:
        try:
            msg = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=_TRANSLATION_SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
            )

            parts = []

            for block in msg.content:
                if getattr(block, "type", None) == "text":
                    parts.append(block.text)

            return "".join(parts).strip() or None

        except Exception as e:
            print("Claude Error:", e)
            return None


def build_translator() -> Translator:
    provider = (
            os.getenv("I18N_PROVIDER")
            or "openai"
    ).lower()

    if provider in {
        "claude",
        "anthropic",
    }:
        return ClaudeTranslate()

    return OpenAITranslate()