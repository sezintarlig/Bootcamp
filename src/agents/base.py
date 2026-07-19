"""Agent temel sınıfı: Gemini çağrısını saran ince katman."""
from __future__ import annotations

import json
import re
import time

from google import genai
from google.genai import types

# Ücretsiz Gemini kotası dakikada 5 istek; 429'da API'nin önerdiği süre kadar beklenir.
MAX_QUOTA_RETRIES = 2
DEFAULT_RETRY_DELAY = 20.0


class AgentError(Exception):
    pass


def _quota_delay(exc: Exception) -> float | None:
    """429/kota hatasıysa beklenecek süreyi döndürür, değilse None."""
    text = str(exc)
    if "429" not in text and "RESOURCE_EXHAUSTED" not in text:
        return None
    match = re.search(r"retry in ([\d.]+)s", text) or re.search(r"retryDelay.{0,5}?([\d.]+)s", text)
    return float(match.group(1)) + 1 if match else DEFAULT_RETRY_DELAY


class GeminiAgent:
    """Her agent'ın kendi adı ve sistem prompt'u vardır; tek sorumluluk taşır."""

    name: str = "agent"
    system_prompt: str = ""

    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model

    def _generate(self, prompt: str, json_output: bool = False) -> str:
        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            response_mime_type="application/json" if json_output else None,
            max_output_tokens=8192,
        )
        for attempt in range(MAX_QUOTA_RETRIES + 1):
            try:
                resp = self.client.models.generate_content(
                    model=self.model, contents=prompt, config=config
                )
                break
            except Exception as exc:
                delay = _quota_delay(exc)
                if delay is None or attempt == MAX_QUOTA_RETRIES:
                    raise AgentError(f"{self.name}: Gemini çağrısı başarısız — {exc}") from exc
                time.sleep(delay)
        if not resp.text:
            raise AgentError(f"{self.name}: modelden boş yanıt döndü.")
        return resp.text

    def run_json(self, prompt: str, retries: int = 1) -> dict:
        last_exc: Exception | None = None
        for _ in range(retries + 1):
            raw = self._generate(prompt, json_output=True)
            try:
                return json.loads(raw.strip().removeprefix("```json").removesuffix("```"))
            except json.JSONDecodeError as exc:
                last_exc = exc
        raise AgentError(f"{self.name}: model geçerli JSON döndürmedi.") from last_exc

    def run_text(self, prompt: str) -> str:
        return self._generate(prompt, json_output=False)
