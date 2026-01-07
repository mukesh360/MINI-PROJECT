import requests

class LLM:
    def __init__(self, model="llama3:latest"):
        self.model = model
        self.url = "http://127.0.0.1:11434/v1/chat/completions"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        response = requests.post(
            self.url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer ollama"  # required dummy value
            },
            timeout=180
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
