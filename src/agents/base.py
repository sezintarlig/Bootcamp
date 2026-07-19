"""Agent temel sınıfı: Gemini çağrısını saran ince katman."""
import json

from google import genai
from google.genai import types


class AgentError(Exception):
    pass


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
        )
        try:
            resp = self.client.models.generate_content(
                model=self.model, contents=prompt, config=config
            )
        except Exception as exc:
            raise AgentError(f"{self.name}: Gemini çağrısı başarısız — {exc}") from exc
        if not resp.text:
            raise AgentError(f"{self.name}: modelden boş yanıt döndü.")
        return resp.text

    def run_json(self, prompt: str) -> dict:
        raw = self._generate(prompt, json_output=True)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AgentError(f"{self.name}: model geçerli JSON döndürmedi.") from exc

    def run_text(self, prompt: str) -> str:
        return self._generate(prompt, json_output=False)
