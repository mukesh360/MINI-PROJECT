from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LLM:
    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        output = self.model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.0,
        )

        return self.tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        ).split("Answer:")[-1].strip()
