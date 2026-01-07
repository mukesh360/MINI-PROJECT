import requests

class LLM:
    def __init__(self, model=None):
        self.model = "llama3:latest"
        self.url = "http://localhost:11434/api/chat"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        # Ollama native response format
        return response.json()["message"]["content"]
